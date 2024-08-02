############################################################
# Dockerfile to build chiron container
# Based on Ubuntu v23.04
############################################################

FROM python:3.10-slim
LABEL authors="Richard A. Schäfer"

# update sources list
RUN apt-get -y update && apt-get install -y
RUN apt-get install -y python3-dev build-essential python3-pip python3-setuptools python3-wheel tree
RUN pip3 install rdata
RUN pip3 install pandas
RUN pip3 install numpy
RUN pip3 install xgboost
RUN pip3 install scikit-learn
RUN pip3 install scikit-optimize
RUN pip3 install shap
RUN pip3 install matplotlib
RUN pip3 install optuna
RUN pip3 install pdbpp
RUN pip3 install configargparse

WORKDIR /usr/local/bin
ADD chiron /chiron
RUN chmod +x /chiron/main.py

ENTRYPOINT [ "python3", "/chiron/main.py", "--input", "/input", "--output", "/output" ]
