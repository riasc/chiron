import rdata
import pandas as pd

class HealthAndExposure:
    def __init__(self, filename, type):
        self.rdata = self.parse_he_rdata(filename, type)

    def parse_he_rdata(self, rdatafile, type):
        converted = rdata.read_rda(str(rdatafile))
        df = next(iter(converted.values())) # convert into dataframe

        # extract fields
        cats = []
        cats.append("epr_number")
        cats.append("he_age_derived") # age (while answering the survey)
        cats.append("he_bmi_cat_derived")
        cats.append("he_a005_physical_health")
        cats.append("he_b007_hypertension_PARQ") # ever diagnosed with hypertension
        cats.append("he_b009_atherosclerosis")
        cats.append("he_b010_cardiac_arrhythmia")
        cats.append("he_b012_heart_attack")
        cats.append("he_b013_coronary_artery")
        cats.append("he_b014_congestive_heart_failure")
        cats.append("he_b015_poor_blood_flow")
        cats.append("he_b016_raynauds")
        cats.append("he_b017_blood_clots")
        cats.append("he_b018_angioplasty")
        cats.append("he_b019_stroke_mini")
        cats.append("he_b020_stroke_PARQ")
        cats.append("he_c022_diabetes_PARQ")
        cats.append("he_c023_thyroid_disease_PARQ")
        cats.append("he_d027_tb_PARQ")
        cats.append("he_d028_cough_breathlessness")
        cats.append("he_d030_asthma_PARQ")
        cats.append("he_e031_epilepsy")
        cats.append("he_e032_migraine")
        cats.append("he_e033_parkinsons")
        cats.append("he_e034_ptsd")
        cats.append("he_e035_alzheimers")
        cats.append("he_e036_ms")
        cats.append("he_f037_celiac")
        cats.append("he_f038_lactose_intolerance")
        cats.append("he_f039_crohns")
        cats.append("he_f040_ulcerative_colitis")
        cats.append("he_f041_polyps")
        cats.append("he_f042_gallbladder_disease")
        cats.append("he_f043_stomach_ulcer")
        cats.append("he_f044_cirrhosis")
        cats.append("he_f045_fatty_liver")
        cats.append("he_f046_hepatitis_PARQ")
        cats.append("he_g047_ckd")
        cats.append("he_g048_esrd")
        cats.append("he_g049_kidney_stones")
        cats.append("he_g050_kidney_infection")
        cats.append("he_g051_pkd")
        cats.append("he_h052_allergic_reactions")
        cats.append("he_h053_scleroderma")
        cats.append("he_h054_shingles")
        cats.append("he_h055_fibromyalgia")
        cats.append("he_h056_lupus")
        cats.append("he_h057_sjogrens")
        cats.append("he_i058_hemochromatosis")
        cats.append("he_i059_iron_anemia")
        cats.append("he_i060_pernicious_anemia")
        cats.append("he_i061_sickle_cell")
        cats.append("he_j062_bone_loss")
        cats.append("he_j063_osteoporosis")
        cats.append("he_j064_gout")
        cats.append("he_j065_myositis")
        cats.append("he_j066_rheu_arthritis_PARQ")
        cats.append("he_j067_osteoarthritis_PARQ")
        cats.append("he_k069_psoriasis")
        cats.append("he_k070_eczema")
        cats.append("he_k071_urticaria")
        cats.append("he_k072_sunburn")
        cats.append("he_k073_scars")
        cats.append("he_l080_chronic_fatigue")
        cats.append("he_o103_cancer_PARQ")
        cats.append("he_q140_asbestos_PARQ")
        cats.append("he_q141_biohazards_PARQ")
        cats.append("he_q142_chemicals_PARQ")
        cats.append("he_q143_coal_dust_PARQ")
        cats.append("he_q144_coal_tar_PARQ")
        cats.append("he_q145_diesel_PARQ")
        cats.append("he_q146_dyes_PARQ")
        cats.append("he_q147_formaldehyde_PARQ")
        cats.append("he_q148_gasoline_PARQ")
        cats.append("he_q149_heavy_metals_PARQ")
        cats.append("he_q150_pesticide_PARQ")
        cats.append("he_q151_sand_PARQ")
        cats.append("he_q152_other_dust_PARQ")
        cats.append("he_q153_textiles_PARQ")
        cats.append("he_q154_wood_dust_PARQ")
        cats.append("he_q155_xrays_PARQ")
        cats.append("he_s185_smoke_indoors")
        cats.append("he_s187_alcohol_life_PARQ")
        cats.append("he_s192_sleep_hours")
        # if type == "train": # only available for training data
        #     cats.append("he_b008_high_cholesterol") # ever diagnosed with high cholesterol

        selected = df[cats]

        # cancer family history
        selected = pd.merge(selected, self.cancer_family_history(df))

        # combine family history - retrieve and merge for different diseases
        selected = pd.merge(selected, self.combine_family_history("he", "166", "diabetes", df), on="epr_number")
        selected = pd.merge(selected, self.combine_family_history("he", "167", "hbp", df), on="epr_number")
        selected = pd.merge(selected, self.combine_family_history("he", "168", "stroke", df), on="epr_number")
        selected = pd.merge(selected, self.combine_family_history("he", "169", "heart_attack", df), on="epr_number")
        selected = pd.merge(selected, self.combine_family_history("he", "170", "coronary_artery", df), on="epr_number")
        selected = pd.merge(selected, self.combine_family_history("he", "171", "sickle_cell", df), on="epr_number")
        selected = pd.merge(selected, self.combine_family_history("he", "172", "rheu_arthritis", df), on="epr_number")
        selected = pd.merge(selected, self.combine_family_history("he", "173", "alzheimers", df), on="epr_number")
        selected = pd.merge(selected, self.combine_family_history("he", "174", "asthma", df), on="epr_number")
        selected = pd.merge(selected, self.combine_family_history("he", "175", "autism", df), on="epr_number")
        selected = pd.merge(selected, self.combine_family_history("he", "176", "hayfever", df), on="epr_number")
        selected = pd.merge(selected, self.combine_family_history("he", "177", "emphysema", df), on="epr_number")
        selected = pd.merge(selected, self.combine_family_history("he", "178", "parkinsons", df), on="epr_number")

        if type == "train":
            target = pd.DataFrame()
            target["epr_number"] = df["epr_number"]
            target["he_b008_high_cholesterol"] = df["he_b008_high_cholesterol"]
            selected = pd.merge(selected, target, on="epr_number")

        return selected

    def parse_expoa_rdata(self, rdatafile, type):
        converted = rdata.read_rda(str(rdatafile))
        df = next(iter(converted.values()))

        # extract
        cats = []
        cats.append("epr_number")
        cats.append("ea_a018_fireplace")
        cats.append("ea_a022_ac")


    def cancer_family_history(self, df):
        """ Combine family history of cancer """
        df_cancer = pd.DataFrame()
        df_cancer["epr_number"] = df["epr_number"]

        cancer_mapping = [
            ("156", "breast_cancer", 1),
            ("157", "colon_cancer", 2),
            ("158", "leukemia", 3),
            ("159", "lung_cancer", 4),
            ("160", "lymphoma", 5),
            ("161", "prostate_cancer", 6),
            ("162", "ovarian_cancer", 7),
            ("163", "melanoma", 8),
            ("164", "skin", 9),
            ("165", "cancer_other", 10)
        ]

        cancer_cols = []
        for cancer in cancer_mapping:
            # combine the family history of different cancer types in one dataframe
            df_cancer = pd.merge(df_cancer, self.combine_family_history("he", cancer[0], cancer[1], df), on="epr_number")
            cancer_cols.append(f"he_r{cancer[0]}_{cancer[1]}_fam")
        df_cancer["he_156-165_cancer_fam"] = df_cancer[cancer_cols].max(axis=1)

        return df_cancer

    def combine_family_history(self, survey, number, diagnosis, df):
        """ Combine parental history into one column """
        mom = f"{survey}_r{number}a_{diagnosis}_mom"
        dad = f"{survey}_r{number}b_{diagnosis}_dad"
        bro = f"{survey}_r{number}c_{diagnosis}_bro_PARQ"
        sis = f"{survey}_r{number}d_{diagnosis}_sis_PARQ"

        if diagnosis == "prostate_cancer":
            all = [dad, bro]
        elif diagnosis == "ovarian_cancer":
            all = [mom, sis]
        else:
            all = [mom, dad, bro, sis]

        fam_df = pd.DataFrame()
        fam_df["epr_number"] = df["epr_number"]
        for col in all:
            fam_df[col] = pd.to_numeric(df[col], errors='coerce')

        fam_col = f"{survey}_r{number}_{diagnosis}_fam"
        fam_df[fam_col] = fam_df[all].max(axis=1)

        # drop the individual columns
        fam_df.drop(columns=all, inplace=True)

        return fam_df
