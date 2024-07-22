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

    # in training data remove epr_number
    hedata_train.rdata.drop(columns=['epr_number'], inplace=True)
    # merge data into one final data.frame
    df = hedata_train.rdata
    df.replace(['.M','.S'], np.nan, inplace=True)
    df = df.map(pd.to_numeric, errors='coerce')

    # load and train the model
    xgboost = model.Model(df)
    xgboost.train()

    hedata_val = surveys.HealthAndExposure(dfiles.he_survey["val"], "val")
    df_val = hedata_val.rdata
    epr_numbers = df_val.pop("epr_number") # save the epr_numbers
    df_val.replace(['.M','.S'], np.nan, inplace=True)
    df_val = df_val.map(pd.to_numeric, errors='coerce')

    # predict probabilities
    prediction = xgboost.predict(df_val)[:,1]
    # create dataframe for output
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
    #p.add_argument("-r", "--ref", help="Folder with reference files", required=True)
    return p.parse_args()

main()
