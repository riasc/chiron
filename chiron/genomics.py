import pandas as pd

class Telomere:
    def __init__(self, xlsxfile, type):
        print()
        self.data = self.parse_xlsx(xlsxfile, type)

    def parse_xlsx(self, xlsxfile, type):
        df = pd.read_excel(xlsxfile)
        # replace column names
        df.columns = ["epr_number", "sampleID", "telomere_content"]
        return df
