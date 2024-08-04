import pandas as pd

class Telomere:
    def __init__(self, xlsxfile, type):
        self.data = self.parse_xlsx(xlsxfile, type)

    def parse_xlsx(self, xlsxfile, type):
        df = pd.read_excel(xlsxfile)
        # replace column names
        df.columns = ["epr_number", "sampleID", "telomere_content"]
        return df

class Ancestry:
    def __init__(self, xlsxfile, type):
        self.data = self.parse_xlsx(xlsxfile, type)

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

        self.data = pd.merge(df_hla_a, df_hla_b, on="epr_number", how="outer")
        self.data = pd.merge(self.data, df_hla_c, on="epr_number", how="outer")

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
