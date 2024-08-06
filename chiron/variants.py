import os
from pathlib import Path
import pandas as pd
import numpy as np
#from bed_reader import open_bed, sample_file
from pysnptools.snpreader import Bed
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
        self.pgs_df = pd.DataFrame(list(self.pgs.items()), columns=['epr_number', 'PGS_Score'])
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
