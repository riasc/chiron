import os
from pathlib import Path
import pandas as pd
import numpy as np
#from bed_reader import open_bed, sample_file
from pysnptools.snpreader import Bed
import vcfpy
from concurrent.futures import ThreadPoolExecutor
import threading

# classes
import helper

class SNVs:
    def __init__(self, bedfile, type, refdir, threads):
        # parse scoring file
        pgs_scoring_file = Path(refdir) / Path("PGS.txt")
        self.parse_pgs_catalog(pgs_scoring_file)
        self.pgs = {}
        self.lock = threading.Lock()
        self.snp_counter = 1
        self.variants = self.parse_snvs(bedfile, threads)

        # create data frame
        self.data = pd.DataFrame(list(self.pgs.items()), columns=['epr_number', 'PGS_Score'])
        print(helper.get_current_time() + "SNV data parsed. (" + type + ")")


    def parse_snvs(self, bedfile, threads):
        bed = Bed(bedfile, count_A1=False)
        sample_ids = bed.iid

        snp_idx = list(range(bed.sid_count))
        self.total_snp = len(snp_idx)

        # chunkgs
        chunk_size = 1000
        snp_chunks = [snp_idx[i:i + chunk_size] for i in range(0, len(snp_idx), chunk_size)]

        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(self.process_snvs, bed, chunk, sample_ids) for chunk in snp_chunks]
            for future in futures:
                future.result()

    def process_snvs(self, bed, chunk, sample_ids):
#        print(f"Process from {chunk[0]} to {chunk[-1]}")
        for snp_idx in chunk:
            snp_id = bed.sid[snp_idx]
            if not snp_id.startswith("rs"):
                continue
            if not snp_id in self.pgs_catalog:
                continue
            genotypes = bed[:, snp_idx].read().val
            weight = self.pgs_catalog[snp_id]

            # extract genotypes for each sample
            for sample_idx, (fid, iid) in enumerate(sample_ids):
                gt = genotypes[sample_idx]
                if int(fid) not in self.pgs:
                    self.pgs[int(fid)] = 0.0

                if not np.isnan(gt[0]):
                    self.pgs[int(fid)] += gt[0] * weight

    def parse_pgs_catalog(self, scoringfile):
        self.pgs_catalog = {}
        fh = open(str(scoringfile), "r")
        for line in fh:
            if line.startswith("#"):
                continue
            fields = line.strip().split("\t")
            # skip header
            if fields[0] == "rsID":
                continue
            self.pgs_catalog[fields[0]] = float(fields[5]) # rsID -> effect_weight
        fh.close()


def format_chromosome(chromosome):
    if chromosome.is_integer():
        snp_chr = str(int(chromosome))
    elif chromosome == 23:
        snp_chr = "X"
    elif chromosome == 24:
        snp_chr = "Y"
    elif chromosome == 25:
        snp_chr = "XY"
    elif chromosome == 26:
        snp_chr = "MT"
    else:
        snp_chr = str(chromosome)
    return snp_chr


class StructuralVariants:
    def __init__(self, vcffile, type, refdata):
        self.genes = self.parse_sig_genes(refdata)
        self.data = self.process_svs(vcffile)

        print(helper.get_current_time() + "SV data parsed. (" + type + ")")

    def process_svs(self, vcffile):
        vcf_reader = vcfpy.Reader.from_path(vcffile)
        # samples
        samples = vcf_reader.header.samples.names

        deletions = {}
        duplications = {}
        inversions = {}

        for record in vcf_reader:
            chr = record.CHROM

            # iterate through significant genes
            for gene in self.genes:
                if self.genes[gene]["chr"] == chr:
                    start = self.genes[gene]["start"]
                    end = self.genes[gene]["end"]
                    if start <= record.POS <= end:
                        svtype = record.INFO["SVTYPE"]
                        for call in record.calls:
                            genotype = call.data.get("GT")
                            sample_id = int(call.sample)
                            if genotype is None:
                                continue
                            if genotype[0] == 0 and genotype[1] == 0:
                                continue
                            else:
                                if svtype == "DEL":
                                    if sample_id not in deletions:
                                        deletions[sample_id] = 0
                                    deletions[sample_id] += 1
                                elif svtype == "DUP":
                                    if sample_id not in duplications:
                                        duplications[sample_id] = 0
                                    duplications[sample_id] += 1
                                elif svtype == "INV":
                                    if sample_id not in inversions:
                                        inversions[sample_id] = 0
                                    inversions[sample_id] += 1

        # create data frames
        deletions_df = pd.DataFrame(list(deletions.items()), columns=['epr_number', 'deletions'])
        duplications_df = pd.DataFrame(list(duplications.items()), columns=['epr_number', 'duplications'])
        inversions_df = pd.DataFrame(list(inversions.items()), columns=['epr_number', 'inversions'])

        # merge intp one
        sv_df = pd.merge(deletions_df, duplications_df, on='epr_number', how='outer')
        sv_df = pd.merge(sv_df, inversions_df, on='epr_number', how='outer')

        return sv_df

        # GT:ADP:CN:DD:EC:ND:RP:SC:SP
        # ##FORMAT=<ID=ADP,Number=1,Type=Float,Description="Approximate read depth (reads with MQ=255 or with bad mates are filtered)">
        ##FORMAT=<ID=CN,Number=1,Type=Integer,Description="Copy Number">
        ##FORMAT=<ID=DD,Number=A,Type=Float,Description="Normalized depth in before, inside first, inside second, and after SV">
        ##FORMAT=<ID=EC,Number=1,Type=Integer,Description="Number of supporting soft clips around end position of SV">
        ##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
        ##FORMAT=<ID=ND,Number=1,Type=Float,Description="Normalized depth">
        ##FORMAT=<ID=RP,Number=1,Type=Integer,Description="Number of supporting read pairs">
        ##FORMAT=<ID=SC,Number=1,Type=Integer,Description="Number of supporting soft clips around starting position of SV">
        ##FORMAT=<ID=SP,Number=1,Type=Integer,Description="Number of supporting split reads">


    def parse_sig_genes(self, refdata):
        genes = {}
        genesbed = Path(refdata) / Path("genes.bed")
        fh = open(str(genesbed))
        for line in fh:
            fields = line.strip().split("\t")
            chr = fields[0]
            start = int(fields[1])
            end = int(fields[2])
            gene = fields[3]
            genes[gene] = {
                "chr": chr,
                "start": start,
                "end": end
            }
        return genes
