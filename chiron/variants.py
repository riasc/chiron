import os
from pathlib import Path
import pandas as pd
import numpy as np
from bed_reader import open_bed, sample_file

class PolygenicScore:
    def __init__(self, options, snvfile):
        pgs_scoringfile = options.ref / Path("PGS000936.txt")
#        self.pgs_catalog = self.parse_pgs_scoringfile(pgs_scoringfile)
#        self.variants = self.parse_snvs(snvfile)
        # self.calculate_pgs(self.variants)

    # def parse_pgs_scoringfile(self, scoringfile):
    #     try:
    #         pgs_catalog = pd.read_csv(scoringfile, sep="\t", comment="#")
    #         return pgs_catalog
    #     except Exception as e:
    #         print(f"Error reading the PGS scoring file: {e}")
    #         return None

    # def parse_snvs(self, snvs):
    #     print(snvs)

    #     bed = open_bed(snvs)
    #     print(bed.read())






        # for record in reader:
        #     variant_id = f"{record.CHROM}:{record.POS}"
        #     for call in record.calls:
        #         sample = call.sample
        #         genotype = call.data.get("GT")
        #         if genotype and genotype != "./.":
        #             if sample not in variants:
        #                 variants[sample] = {}
        #             variants[sample][variant_id] = {
        #                 "genotype": genotype.split("/"),
        #                 "ref": record.REF,
        #                 "alt": record.ALT
        #             }
        # return variants

    # def calculate_pgs(self, variants):
    #     pgs_score = 0
    #     scores = {}
    #     for idx, row in self.pgs_catalog.iterrows():
    #         variant_id = f"chr{row['chr_name']}:{row['pos']}"
    #         effect_allele = row["effect_allele"]
    #         weight = row["effect_weight"]

    #         for sample, variant in variants.items():
    #             if variant_






    #     breakpoint()
    #     print(variants)
