import os
from pathlib import Path
import configargparse
import rdata
import random
import pandas as pd
import numpy as np

# classes
import variants
import general
import genomics
import surveys
import model
import helper

def main():
    options = parse_arguments()
    print(helper.get_current_time() + "Chiron - Starting the prediction using the defined parameters")
    dfiles = general.DataFiles(options.input, options.synthetic)

    hedata_train = surveys.HealthAndExposure(dfiles.he_survey["train"], "train")
    eadata_train = surveys.Exposome(dfiles.expoa_survey["train"], "train", "exposome_a")
    ebdata_train = surveys.Exposome(dfiles.expob_survey["train"], "train", "exposome_b")
    snvsdata_train = variants.SNVs(dfiles.snvs_data["train"], "train", options.ref, options.threads)
    telomere_train = genomics.Telomere(dfiles.telomere_data["train"], "train")
    ancestry_train = genomics.Ancestry(dfiles.ancestry_data["train"], "train")
    hladata_train = genomics.genotyping(dfiles.hla_data["train"], "train")
    methdata_train = genomics.Methylation(dfiles.meth_data["train"], "train", options.ref)
    structvardata_train = variants.StructuralVariants(dfiles.sv_data["train"], "train", options.ref)

    # merge into one data.
    df_train = hedata_train.rdata
    df_train = pd.merge(df_train, eadata_train.data, on="epr_number", how="outer")
    df_train = pd.merge(df_train, ebdata_train.data, on="epr_number", how="outer")
    df_train = pd.merge(df_train, snvsdata_train.data, on="epr_number", how="outer")
    df_train = pd.merge(df_train, telomere_train.data, on="epr_number", how="outer")
    df_train = pd.merge(df_train, ancestry_train.data, on="epr_number", how="outer")
    df_train = pd.merge(df_train, hladata_train.data, on="epr_number", how="outer")
    df_train = pd.merge(df_train, methdata_train.data, on="epr_number", how="outer")
    df_train = pd.merge(df_train, structvardata_train.data, on="epr_number", how="outer")

    # save train data
    output_path = Path(options.output) / Path("training_data.csv")
    df_train.to_csv(output_path, index=False)

    # preprocess data
    df_train.replace(['.M','.S'], np.nan, inplace=True) # replace missing values
    df_train.drop(columns=['epr_number'], inplace=True)
    df_train = df_train.map(pd.to_numeric, errors='coerce')
    df_train.replace(-888888, np.nan, inplace=True)
    print(helper.get_current_time() + "Training data loaded and preprocessed")

    print(helper.get_current_time() + "Training the model")
    # load and train the model
    gradboost = model.Model(df_train, options)
    gradboost.train()

    if options.explain:
        gradboost.explain()

    hedata_val = surveys.HealthAndExposure(dfiles.he_survey["val"], "val")
    eadata_val = surveys.Exposome(dfiles.expoa_survey["val"], "val", "exposome_a")
    ebdata_val = surveys.Exposome(dfiles.expob_survey["val"], "val", "exposome_b")
    snvsdata_val = variants.SNVs(dfiles.snvs_data["val"], "val", options.ref, options.threads)
    telomere_val = genomics.Telomere(dfiles.telomere_data["val"], "val")
    ancestry_val = genomics.Ancestry(dfiles.ancestry_data["val"], "val")
    hladata_val = genomics.genotyping(dfiles.hla_data["val"], "val")
    methdata_val = genomics.Methylation(dfiles.meth_data["val"], "val", options.ref)
    structvardata_val = variants.StructuralVariants(dfiles.sv_data["val"], "val", options.ref)

    # merge into one data.frame
    df_val = hedata_val.rdata
    df_val = pd.merge(df_val, eadata_val.data, on="epr_number", how="outer")
    df_val = pd.merge(df_val, ebdata_val.data, on="epr_number", how="outer")
    df_val = pd.merge(df_val, snvsdata_val.data, on="epr_number", how="outer")
    df_val = pd.merge(df_val, telomere_val.data, on="epr_number", how="outer")
    df_val = pd.merge(df_val, ancestry_val.data, on="epr_number", how="outer")
    df_val = pd.merge(df_val, hladata_val.data, on="epr_number", how="outer")
    df_val = pd.merge(df_val, methdata_val.data, on="epr_number", how="outer")
    df_val = pd.merge(df_val, structvardata_val.data, on="epr_number", how="outer")
    print(helper.get_current_time() + "Validation data loaded and preprocessed")

    # save val data
    output_path = Path(options.output) / Path("train_data.csv")
    df_val.to_csv(output_path, index=False)

    df_val.replace(['.M','.S'], np.nan, inplace=True) # replace missing values

    epr_numbers = df_val.pop("epr_number") # save the epr_numbers
    df_val = df_val.map(pd.to_numeric, errors='coerce')

    # predict probabilities
    print(helper.get_current_time() + "Predict disease probabilities")
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
    p.add_argument("-e", "--explain", action="store_true", help="Explain the model", required=False)
    p.add_argument("-c", "--challenge", action="store_true", help="Challenge mode", required=False)
    p.add_argument("-t", "--threads", help="Number of threads", required=False, default=1, type=int)
    return p.parse_args()

main()
