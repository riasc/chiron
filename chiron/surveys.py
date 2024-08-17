import os
import rdata
import pandas as pd
import subprocess
import tempfile

# classes
import helper

class HealthAndExposure:
    def __init__(self, filename, type):
        self.rdata = self.parse_he_rdata(filename, type)
        print(helper.get_current_time() + "Health and Exposure data parsed. (" + type + ")")

    def parse_he_rdata(self, rdatafile, type):
        converted = rdata.read_rda(str(rdatafile))
        df = next(iter(converted.values())) # convert into dataframe

        conts = [
            "he_age_derived", # age (while answering the survey)
            "he_s192_sleep_hours"
        ]

        cats = [
            "he_bmi_cat_derived",
            "he_a005_physical_health",
            "he_b007_hypertension_PARQ", # ever diagnosed with hypertension
            "he_b009_atherosclerosis",
            "he_b010_cardiac_arrhythmia",
            "he_b012_heart_attack",
            "he_b013_coronary_artery",
            "he_b014_congestive_heart_failure",
            "he_b015_poor_blood_flow",
            "he_b016_raynauds",
            "he_b017_blood_clots",
            "he_b018_angioplasty",
            "he_b019_stroke_mini",
            "he_b020_stroke_PARQ",
            "he_c022_diabetes_PARQ",
            "he_c023_thyroid_disease_PARQ",
            "he_d027_tb_PARQ",
            "he_d028_cough_breathlessness",
            "he_d030_asthma_PARQ",
            #"he_e031_epilepsy",
            "he_e032_migraine",
            #"he_e033_parkinsons",
            #"he_e034_ptsd",
            #"he_e035_alzheimers",
            "he_e036_ms",
            #"he_f037_celiac",
           # "he_f038_lactose_intolerance",
            #"he_f039_crohns",
            "he_f040_ulcerative_colitis",
            "he_f041_polyps",
            "he_f042_gallbladder_disease",
            "he_f043_stomach_ulcer",
            #"he_f044_cirrhosis",
            "he_f045_fatty_liver",
            #"he_f046_hepatitis_PARQ",
            "he_g047_ckd",
            #"he_g048_esrd",
            #"he_g049_kidney_stones",
            "he_g050_kidney_infection",
            #"he_g051_pkd",
            "he_h052_allergic_reactions",
            #"he_h053_scleroderma",
           # "he_h054_shingles",
            "he_h055_fibromyalgia",
            "he_h056_lupus",
            #"he_h057_sjogrens",
            #"he_i058_hemochromatosis",
            "he_i059_iron_anemia",
            #"he_i060_pernicious_anemia",
            #"he_i061_sickle_cell",
            "he_j062_bone_loss",
            "he_j063_osteoporosis",
            "he_j064_gout",
            #"he_j065_myositis",
            "he_j066_rheu_arthritis_PARQ",
            "he_j067_osteoarthritis_PARQ",
            "he_k069_psoriasis",
            "he_k070_eczema",
            "he_k071_urticaria",
            "he_k072_sunburn",
            #"he_k073_scars",
            "he_l080_chronic_fatigue",
            "he_o103_cancer_PARQ",
            "he_q140_asbestos_PARQ",
            "he_q141_biohazards_PARQ",
            "he_q142_chemicals_PARQ",
            "he_q143_coal_dust_PARQ",
            "he_q144_coal_tar_PARQ",
            #"he_q145_diesel_PARQ",
            "he_q146_dyes_PARQ",
            "he_q147_formaldehyde_PARQ",
            #"he_q148_gasoline_PARQ",
            "he_q149_heavy_metals_PARQ",
            "he_q150_pesticide_PARQ",
            #"he_q151_sand_PARQ",
            #"he_q152_other_dust_PARQ",
            #"he_q153_textiles_PARQ",
            #"he_q154_wood_dust_PARQ",
            #"he_q155_xrays_PARQ",
            "he_s185_smoke_indoors",
            "he_s187_alcohol_life_PARQ"
        ]

        selected = df[["epr_number"] + conts + cats]

        # cancer family history
        selected = pd.merge(selected, self.cancer_family_history(df))
        cats.append("he_156-165_cancer_fam")

        diagnosis = [
            ("166", "diabetes"),
            ("167", "hbp"),
            ("168", "stroke"),
            ("169", "heart_attack"),
            ("170", "coronary_artery"),
            ("171", "sickle_cell"),
            ("172", "rheu_arthritis"),
            ("173", "alzheimers"),
            ("174", "asthma"),
            ("175", "autism"),
            ("176", "hayfever"),
            ("177", "emphysema"),
            ("178", "parkinsons")
        ]

        # combine family history - retrieve and merge for different diseases
        for code, disease in diagnosis:
            selected = pd.merge(selected, self.combine_family_history("he", code, disease, df), on="epr_number")
            cats.append(f"he_r{code}_{disease}_fam")

        if type == "train":
            target = pd.DataFrame()
            target["epr_number"] = df["epr_number"]
            target["he_b008_high_cholesterol"] = df["he_b008_high_cholesterol"]
            selected = pd.merge(selected, target, on="epr_number")
            cats.append("he_b008_high_cholesterol")

        # categorize
        # for col in cats:
        #     selected[col] = selected[col].astype("category")

        return selected

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

        df_final = pd.DataFrame()
        df_final["epr_number"] = df["epr_number"]
        df_final["he_156-165_cancer_fam"] = df_cancer[cancer_cols].max(axis=1)

        return df_final

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

class Exposome:
    def __init__(self, filename, type, exposome_type):
        if exposome_type == "exposome_a":
            self.rdata = self.parse_expoa_rdata(filename, exposome_type)
            print(helper.get_current_time() + "Exposome A data parsed. (" + type + ")")
        elif exposome_type == "exposome_b":
            self.rdata = self.parse_expob_rdata(filename, exposome_type)
            print(helper.get_current_time() + "Exposome B data parsed. (" + type + ")")

    def parse_expoa_rdata(self, rdatafile, type):
        converted = rdata.read_rda(str(rdatafile))
        df = next(iter(converted.values())) # convert into dataframe

        # extract
        cats = [
            "ea_a018_fireplace_PARQ",
            "ea_a022_ac_PARQ",
            "ea_a040_mold_derived",
            "ea_a046_carpet_PARQ",
            "ea_a058_pet_PARQ",
            "ea_a067_animal_waste"
        ]

        selected = df[["epr_number"] + cats]
        return selected

    def parse_expob_rdata(self, rdatafile, exposome_type):
        exposome2csv_path = os.path.join(os.path.dirname(__file__), 'exposome2csv.R')
        df = pd.DataFrame()
        with tempfile.NamedTemporaryFile() as csv_file:
            subprocess.run(["Rscript", exposome2csv_path, rdatafile, csv_file.name, exposome_type])
            df = pd.read_csv(csv_file.name)

        # print to file for testing
        df.to_csv("exposome_b.csv", index=False)

        cats = [
            "eb_a001_multivitamin_PARQ",
            "eb_a002_vitamin_a_PARQ",
            "eb_a003_vitamin_b3_PARQ",
            "eb_a004_vitamin_b6_PARQ",
            "eb_a005_vitamin_b12_PARQ",
            "eb_a006_vitamin_b_comp_PARQ",
            "eb_a007_vitamin_c_PARQ",
            "eb_a008_vitamin_d_PARQ",
            "eb_a009_vitamin_e_PARQ",
            "eb_a010_calcium_PARQ",
            "eb_a011_chromium_PARQ",
            "eb_a012_iron_PARQ",
            "eb_a013_magnesium_PARQ",
            "eb_a014_potassium_PARQ",
            "eb_a015_selenium_PARQ",
            "eb_a016_zinc_PARQ",
            "eb_a017_blk_cohosh_PARQ",
            "eb_a018_coq10_PARQ",
            "eb_a019_fish_oil_PARQ",
            "eb_a020_flaxseed_oil_PARQ",
            "eb_g136_wkday_sleep_hrs",
            "eb_h161_fastfood",
            "eb_h164_takeout",
            "eb_i174_milk_whole",
            "eb_i175_milk_nondairy",
            "eb_i176_cream",
            "eb_i180_butter",
            "eb_i190_cheese_regular",
            "eb_i192_avocado",
            "eb_i194_blueberries",
            "eb_i207_beans_lentils",
            "eb_i209_broccoli",
            "eb_i220_spinach_raw",
            "eb_i225_eggs",
            "eb_i229_bacon",
            "eb_i230_deli_meats",
            "eb_i231_other_processed_meat",
            "eb_i232_hamburger",
            "eb_i234_ham",
            "eb_i235_canned_tuna",
            "eb_i240_oatmeal",
            "eb_i246_whole_wheat",
            "eb_i254_fries",
            "eb_i256_pizza",
            "eb_i278_other_nuts",
            "eb_k293_blood_type",
            "eb_k299a_hyperlipidemia_you",
            "eb_k301a_clot_prob_you",
            "eb_k307a_sickle_cell_you",
        ]

        selected = df[["epr_number"] + cats]
        return selected


        # parsed_data = rdata.parser.parse_file(str(rdatafile))
        # converted = rdata.conversion.convert(parsed_data)

        # df = next(iter(converted.values())) # convert into dataframe

        # # extract
        # cats = [
        #     "eb_a019_fish_oil_PARQ",
        #     "eb_a020_flaxseed_oil_PARQ",
        #     "eb_a021_folic_acid_PARQ",
        #     "eb_a022_gingko_biloba_PARQ"
        # ]

        # selected = df[["epr_number"] + cats]
        # return selected
