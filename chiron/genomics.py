import os
import pandas as pd
import subprocess
from pathlib import Path

# classes
import helper

class Telomere:
    def __init__(self, xlsxfile, type):
        self.data = self.parse_xlsx(xlsxfile, type)
        print(helper.get_current_time() + "Telomere data parsed. (" + type + ")")

    def parse_xlsx(self, xlsxfile, type):
        df = pd.read_excel(xlsxfile)
        # replace column names
        df.columns = ["epr_number", "sampleID", "telomere_content"]
        return df

class Ancestry:
    def __init__(self, xlsxfile, type):
        self.data = self.parse_xlsx(xlsxfile, type)
        print(helper.get_current_time() + "Ancestry data parsed. (" + type + ")")

    def parse_xlsx(self, xlsxfile, type):
        df = pd.read_excel(xlsxfile)
        # replace column names
        df.columns = ["epr_number", "sampleID", "ancestry_AFR", "ancestry_AMR", "ancestry_EAS", "ancestry_EUR", "ancestry_SAS"]
        return df

class genotyping:
    def __init__(self, hlafiles, type):
        df_hla_a = self.parse_hladata(hlafiles["HLA-A"], "HLA-A")
        df_hla_b = self.parse_hladata(hlafiles["HLA-B"], "HLA-B")
        df_hla_c = self.parse_hladata(hlafiles["HLA-C"], "HLA-C")
        df_hla_dma = self.parse_hladata(hlafiles["HLA-DMA"], "HLA-DMA")
        df_hla_dmb = self.parse_hladata(hlafiles["HLA-DMB"], "HLA-DMB")
        df_hla_doa = self.parse_hladata(hlafiles["HLA-DOA"], "HLA-DOA")
        df_hla_dob = self.parse_hladata(hlafiles["HLA-DOB"], "HLA-DOB")
        df_hla_dpa1 = self.parse_hladata(hlafiles["HLA-DPA1"], "HLA-DPA1")
        df_hla_dpb1 = self.parse_hladata(hlafiles["HLA-DPB1"], "HLA-DPB1")
        df_hla_dqa1 = self.parse_hladata(hlafiles["HLA-DQA1"], "HLA-DQA1")
        df_hla_dqb1 = self.parse_hladata(hlafiles["HLA-DQB1"], "HLA-DQB1")
        df_hla_dra = self.parse_hladata(hlafiles["HLA-DRA"], "HLA-DRA")
        df_hla_drb1 = self.parse_hladata(hlafiles["HLA-DRB1"], "HLA-DRB1")
        df_hla_drb3 = self.parse_hladata(hlafiles["HLA-DRB3"], "HLA-DRB3")
        df_hla_drb5 = self.parse_hladata(hlafiles["HLA-DRB5"], "HLA-DRB5")
        df_hla_f = self.parse_hladata(hlafiles["HLA-F"], "HLA-F")
        df_hla_g = self.parse_hladata(hlafiles["HLA-G"], "HLA-G")
        df_hla_h = self.parse_hladata(hlafiles["HLA-H"], "HLA-H")
        df_hla_j = self.parse_hladata(hlafiles["HLA-J"], "HLA-J")
        dh_hla_l = self.parse_hladata(hlafiles["HLA-L"], "HLA-L")

        self.data = pd.merge(df_hla_a, df_hla_b, on="epr_number", how="outer")
        self.data = pd.merge(self.data, df_hla_c, on="epr_number", how="outer")
        self.data = pd.merge(self.data, df_hla_dma, on="epr_number", how="outer")
        self.data = pd.merge(self.data, df_hla_dmb, on="epr_number", how="outer")
        self.data = pd.merge(self.data, df_hla_doa, on="epr_number", how="outer")
        self.data = pd.merge(self.data, df_hla_dob, on="epr_number", how="outer")
        self.data = pd.merge(self.data, df_hla_dpa1, on="epr_number", how="outer")
        self.data = pd.merge(self.data, df_hla_dpb1, on="epr_number", how="outer")
        self.data = pd.merge(self.data, df_hla_dqa1, on="epr_number", how="outer")
        self.data = pd.merge(self.data, df_hla_dqb1, on="epr_number", how="outer")
        self.data = pd.merge(self.data, df_hla_dra, on="epr_number", how="outer")
        self.data = pd.merge(self.data, df_hla_drb1, on="epr_number", how="outer")
        self.data = pd.merge(self.data, df_hla_drb3, on="epr_number", how="outer")
        self.data = pd.merge(self.data, df_hla_drb5, on="epr_number", how="outer")
        self.data = pd.merge(self.data, df_hla_f, on="epr_number", how="outer")
        self.data = pd.merge(self.data, df_hla_g, on="epr_number", how="outer")
        self.data = pd.merge(self.data, df_hla_h, on="epr_number", how="outer")
        self.data = pd.merge(self.data, df_hla_j, on="epr_number", how="outer")
        self.data = pd.merge(self.data, dh_hla_l, on="epr_number", how="outer")

    def parse_hladata(self, hlafile, alleletype):
        alleles = {}
        alleles_counter = 0

        # create empty data frame
        df = pd.DataFrame(columns=["epr_number", alleletype + "-Allele1", alleletype + "-Allele2"])

        with open(hlafile, "r") as fh:
            next(fh)
            for line in fh:
                splitted = line.strip().split("\t")
                epr = int(splitted[0])
                al1 = splitted[2].rstrip()
                al2 = splitted[3].rstrip()

                if al1 not in alleles:
                    alleles[al1] = alleles_counter
                    alleles_counter += 1

                if al2 not in alleles:
                    alleles[al2] = alleles_counter
                    alleles_counter += 1

                new_row = {"epr_number": epr, alleletype + "-Allele1": alleles[al1], alleletype + "-Allele2": alleles[al2]}
                df.loc[len(df)] = new_row

        return df

class Methylation:
    def __init__(self, methfile, type, refdata):
        self.data = self.parse_methdata(methfile, type, refdata)
        print(helper.get_current_time() + "Methylation data parsed. (" + type + ")")

    def parse_methdata(self, methfile, type, refdata):
        # create output .csv
        rds2csv_path = os.path.join(os.path.dirname(__file__), 'rds2csv.R')
        csv_file = Path(refdata) / Path("methylation.csv")
        subprocess.run(["Rscript", rds2csv_path , methfile, csv_file])
        df = pd.read_csv(csv_file)

        sums = df.sum(numeric_only=True)
        sums_int = sums.astype(int)

        # create new data.frame
        results_df = pd.DataFrame({
            "epr_number": sums_int,
            "methylation": sums.values
        })

        subprocess.run(["rm", csv_file])
        return results_df
