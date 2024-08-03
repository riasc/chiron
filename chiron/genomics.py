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
