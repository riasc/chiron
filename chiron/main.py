import configargparse
import pyreadr

def main():
    options = parse_arguments()

    print(options)

    survey = parse_survey_file(options.survey)

    print(survey)



def parse_survey_file(survey_file):
    df = pyreadr.read_r(survey_file)

def parse_arguments():
    p = configargparse.ArgParser()
    # define the parameters
    p.add_argument("-s", "--survey", help="Survey files", required=True)

    return p.parse_args()

main()
