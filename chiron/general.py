from pathlib import Path

class DataFiles:
    def __init__(self, input, synthetic):
        self.he_survey = {} # health and exposure survey data
        self.he_survey["train"] = self.get_he_surveyfile(input, "train", synthetic)
        self.he_survey["val"] = self.get_he_surveyfile(input, "val", synthetic)

        self.expoa_survey = {}
        self.expoa_survey["train"] = self.get_expoa_surveyfile(input, "train", synthetic)
        self.expoa_survey["val"] = self.get_expoa_surveyfile(input, "val", synthetic)

        self.expob_survey = {}
        self.expob_survey["train"] = self.get_expob_surveyfile(input, "train", synthetic)
        self.expob_survey["val"] = self.get_expob_surveyfile(input, "val", synthetic)

        self.sv_data = {} # structural variant data
        self.sv_data["train"] = self.get_sv_datafile(input, "train", synthetic)
        self.sv_data["val"] = self.get_sv_datafile(input, "val", synthetic)

        self.snvs_data = {} # single nucleotide variant data
        self.snvs_data["train"] = self.get_snvs_bedfile(input, "train", synthetic)
        self.snvs_data["val"] = self.get_snvs_bedfile(input, "val", synthetic)

        self.telomere_data = {} # telomere data
        self.telomere_data["train"] = self.get_telomere_datafile(input, "train", synthetic)
        self.telomere_data["val"] = self.get_telomere_datafile(input, "val", synthetic)

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

    def get_expoa_surveyfile(self, input, type, synthetic):
        if synthetic:
            data = Path(input) / Path(type + "_data_synthetic")
        else:
            data = Path(input) / Path(type + "_data")
        surveypath = data / Path("PEGS_freeze_v3.1_nonpii") / Path("Surveys") / Path("Exposome")
        if synthetic:
            return surveypath / Path("exposomea_29jul22_v3.1_nonpii_" + type + "_synthetic.RData")
        else:
            return surveypath / Path("exposomea_29jul22_v3.1_nonpii_" + type + ".RData")

    def get_expob_surveyfile(self, input, type, synthetic):
        if synthetic:
            data = Path(input) / Path(type + "_data_synthetic")
        else:
            data = Path(input) / Path(type + "_data")
        surveypath = data / Path("PEGS_freeze_v3.1_nonpii") / Path("Surveys") / Path("Exposome")
        if synthetic:
            return surveypath / Path("exposomeb_29jul22_v3.1_nonpii_" + type + "_synthetic.RData")
        else:
            return surveypath / Path("exposomeb_29jul22_v3.1_nonpii_" + type + ".RData")

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

    def get_telomere_datafile(self, input, type, synthetic):
        if synthetic:
            data = Path(input) / Path(type + "_data_synthetic")
        else:
            data = Path(input) / Path(type + "_data")
        telomerepath = data / Path("PEGS_genomic_data") / Path("telomere_content")
        if synthetic:
            return telomerepath / Path("PEGS_telomere_content_estimates_" + type + "_synthetic.xlsx")
        else:
            return telomerepath / Path("PEGS_telomere_content_estimates_" + type + ".xlsx")

    def get_ancestry_datafile(self, input, type, synthetic):
        if synthetic:
            data = Path(input) / Path(type + "_data_synthetic")
        else:
            data = Path(input) / Path(type + "_data")
        ancestrypath = data / Path("PEGS_genomic_data") / Path("local_ancestry")
        if synthetic:
            return ancestrypath / Path("PEGS_Estimated_Ancestry_Fractions_" + type + "_synthetic.xlsx")
        else:
            return ancestrypath / Path("PEGS_Estimated_Ancestry_Fractions_" + type + ".xlsx")
