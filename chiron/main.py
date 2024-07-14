import os
from pathlib import Path
import configargparse
import rdata
import random


def main():
    options = parse_arguments()

    # get survey data
    survey = parse_survey(options.input, options.type)

    df = next(iter(survey.values()))

    # Extract the first column
    first_column = df.iloc[:, 0]

    # prepare output
    folder_exists(options.output)
    df = open(Path(options.output / Path("predictions.csv")), "w")

    for x in first_column:
        df.write(str(x))
        df.write(",")
        df.write(str(random.random()))
        df.write("\n")


def folder_exists(folder):
    path = Path(folder)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

def parse_survey(input, type):
    exposomeA = Path(input) / Path("exposomea_29jul22_v3.1_nonpii_" + type + "_synthetic.RData")
    converted = rdata.read_rda(str(exposomeA))
    return converted


def parse_arguments():
    p = configargparse.ArgParser()
    # define the parameters
    p.add_argument("-i", "--input", help="Survey files", required=True)
    p.add_argument("-t", "--type", help="Type of data (e.g, train/val)", required=True)
    p.add_argument("-o", "--output", help="Output file", required=True)

    return p.parse_args()

main()
