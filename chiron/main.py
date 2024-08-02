import os
from pathlib import Path
import configargparse
import rdata
import random
import pandas as pd
import numpy as np
#import pdb

# classes
import variants
import general
import surveys
import model

def main():
    options = parse_arguments()

    dfiles = general.DataFiles(options.input, options.synthetic)
    hedata_train = surveys.HealthAndExposure(dfiles.he_survey["train"], "train")
    eadata_train = surveys.Exposome(dfiles.expoa_survey["train"], "train", "exposome_a")
    #ebdata_train = surveys.Exposome(dfiles.expob_survey["train"], "train", "exposome_b")
    snvsdata_train = variants.SNVs(dfiles.snvs_data["train"], "train", options.ref, options.threads)

    # merge the surveys
    df_train = pd.merge(hedata_train.rdata, eadata_train.rdata, on="epr_number", how="outer")
#    df_train = hedata_train.rdata
    df_train.replace(['.M','.S'], np.nan, inplace=True) # replace missing values
    # in training data remove epr_number
    df_train.drop(columns=['epr_number'], inplace=True)

    # merge data into one final data.frame
#    df = hedata_train.rdata
    # cats_cols = df.select_dtypes(["category"]).columns # get the categorical columns
    # df[cats_cols] = df[cats_cols].astype(str) # convert to string
#    df.replace(['.M','.S'], np.nan, inplace=True) # replace missing values
    # df[cats_cols] = df[cats_cols].astype("category") # convert to back to category
    df_train = df_train.map(pd.to_numeric, errors='coerce')
    df_train.replace(-888888, np.nan, inplace=True)

    # load and train the model
    gradboost = model.Model(df_train)
    gradboost.train()

    if options.synthetic:
        gradboost.explain()




    # xgboost.train()

    hedata_val = surveys.HealthAndExposure(dfiles.he_survey["val"], "val")
    eadata_val = surveys.Exposome(dfiles.expoa_survey["val"], "val", "exposome_a")
    #ebdata_val = surveys.Exposome(dfiles.expob_survey["val"], "val", "exposome_b")
    # merge
    df_val = pd.merge(hedata_val.rdata, eadata_val.rdata, on="epr_number", how="outer")
    #df_val = hedata_val.rdata
    df_val.replace(['.M','.S'], np.nan, inplace=True) # replace missing values
    epr_numbers = df_val.pop("epr_number") # save the epr_numbers
    df_val = df_val.map(pd.to_numeric, errors='coerce')

    # predict probabilities
    prediction = gradboost.predict(df_val)

    #create dataframe for output
    df_out = pd.DataFrame({
        "epr_number": epr_numbers,
        "disease_probability": prediction
    })
    # save output
    output_path = Path(options.output) / Path("predictions.csv")
    df_out.to_csv(output_path, index=False)

def folder_exists(folder):
    path = Path(folder)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

def parse_arguments():
    p = configargparse.ArgParser()
    # define the parameters
    p.add_argument("-i", "--input", help="Survey files", required=True)
    p.add_argument("-s", "--synthetic", action="store_true", default=False, help="Use of synthetic data", required=False)
    p.add_argument("-o", "--output", help="Output file", required=True)
    p.add_argument("-r", "--ref", help="Folder with reference files", required=True)
    p.add_argument("-t", "--threads", help="Number of threads", required=False, default=1, type=int)
    return p.parse_args()

main()
