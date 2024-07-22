import os
from pathlib import Path
import configargparse
import rdata
import random
import pandas as pd
#import pdb


# classes
import variants
import general
import surveys

def main():
    options = parse_arguments()

    dfiles = general.DataFiles(options.input, options.synthetic)

    hedata = surveys.HealthAndExposure(dfiles.he_survey["train"], "train")

    # print(dfiles.he_survey["train"])
    # print(dfiles.he_survey["val"])
    # print(dfiles.sv_data["train"])
    # print(dfiles.sv_data["val"])
    #snvs = variants.PolygenicScore(options, dfiles.snvs_data["train"])









    # get survey data
    # survey = parse_survey(options.input, "val", options.datatype)
    # df = next(iter(survey.values()))

    #breakpoint()

    # extract multiple columns
    # cats = []
    # cats.append("epr_number")
    # cats.append("he_age_derived") # age (while answering the survey)
    # cats.append("he_b007_hypertension_PARQ") # ever diagnosed with hypertension
    # cats.append("he_b008_high_cholesterol") # ever diagnosed with high cholesterol


    # print(df[cats])



    # Extract the first column
    # first_column = df.iloc[:, 0]

    # # prepare output
    # folder_exists(options.output)
    # df = open(Path(options.output / Path("predictions.csv")), "w")

    # df.write("epr_number,disease_probability\n")
    # for x in first_column:
    #     df.write(str(x))
    #     df.write(",")
    #     df.write(str(random.random()))
    #     df.write("\n")
    # df.close()

def folder_exists(folder):
    path = Path(folder)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)



# def parse_survey(input, settype, datatype):
#     if datatype == "synthetic":
#         datainfo = "_synthetic"
#     else:
#         datainfo = ""

#     datapath = Path(input) / Path(settype + "_data" + datainfo)
#     surveypath = datapath / Path("PEGS_freeze_v3.1_nonpii") / Path("Surveys")
#     exposomeA = surveypath / Path("Health_and_Exposure") / Path("healthexposure_16jun22_v3.1_nonpii_" + settype + datainfo + ".RData")
#     converted = rdata.read_rda(str(exposomeA))
#     return converted

def parse_arguments():
    p = configargparse.ArgParser()
    # define the parameters
    p.add_argument("-i", "--input", help="Survey files", required=True)
    p.add_argument("-s", "--synthetic", action="store_true", default=False, help="Use of synthetic data", required=False)
    p.add_argument("-o", "--output", help="Output file", required=True)
    p.add_argument("-r", "--ref", help="Folder with reference files", required=True)
    return p.parse_args()

main()
