from pathlib import Path

class DataFiles:
    def __init__(self, input, synthetic):
        self.he_survey = {} # health and exposure survey data
        self.he_survey["train"] = self.get_he_surveyfile(input, "train", synthetic)
        self.he_survey["val"] = self.get_he_surveyfile(input, "val", synthetic)

        self.sv_data = {} # structural variant data
        self.sv_data["train"] = self.get_sv_datafile(input, "train", synthetic)
        self.sv_data["val"] = self.get_sv_datafile(input, "val", synthetic)

        self.snvs_data = {} # single nucleotide variant data
        self.snvs_data["train"] = self.get_snvs_bedfile(input, "train", synthetic)
        self.snvs_data["val"] = self.get_snvs_bedfile(input, "val", synthetic)

    def get_he_surveyfile(self, input, type, synthetic):
        if synthetic:
            data = Path(input) / Path(type + "_data_synthetic")
        else:
            data = Path(input) / Path(type + "_data")
        surveypath = data / Path("PEGS_freeze_v3.1_nonpii") / Path("Surveys") / Path("Health_and_Exposure")
        if synthetic:
            return surveypath / Path("healthexposure_16jun22_v3.1_nonpii_" + type + "_synthetic.RData")
        else:
            return surveypath / Path("healthexposure_16jun22_v3.1_nonpii_" + type + ".RData")

    def get_sv_datafile(self, input, type, synthetic):
        if synthetic:
            data = Path(input) / Path(type + "_data_synthetic")
        else:
            data = Path(input) / Path(type + "_data")
        svpath = data / Path("PEGS_genomic_data") / Path("structural_variants")
        if synthetic:
            return svpath / Path("PEGS_SV_genotypes_" + type + "_synthetic.vcf.gz")
        else:
            return svpath / Path("PEGS_SV_genotypes_" + type + ".vcf.gz")

    def get_snvs_bedfile(self, input, type, synthetic):
        if synthetic:
            data = Path(input) / Path(type + "_data_synthetic")
        else:
            data = Path(input) / Path(type + "_data")
        snvpath = data / Path("PEGS_genomic_data") / Path("SNVs_small_indels")
        if synthetic:
            return snvpath / Path("PEGS_GWAS_genotypes_v1.1_" + type + "_synthetic.bed")
        else:
            return snvpath / Path("PEGS_GWAS_genotypes_v1.1_" + type + ".bed")
