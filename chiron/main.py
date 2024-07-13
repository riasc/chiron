import configargparse
import rdata
import os
from pathlib import Path
import random


def main():
    options = parse_arguments()

    survey = parse_survey_file(options.survey)
    df = next(iter(survey.values()))

    # Extract the first column
    first_column = df.iloc[:, 0]

    for x in first_column:
        print(x)

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

def parse_survey_file(survey_file):
    converted = rdata.read_rda(survey_file)
    return converted


def parse_arguments():
    p = configargparse.ArgParser()
    # define the parameters
    p.add_argument("-s", "--survey", help="Survey files", required=True)
    p.add_argument("-o", "--output", help="Output file", required=True)

    return p.parse_args()

main()
