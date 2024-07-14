############################################################
# Dockerfile to build chiron container
# Based on Ubuntu v23.04
############################################################

FROM python:3.9.19-slim
LABEL authors="Richard A. Schäfer"

# update sources list
RUN apt-get -y update && apt-get install -y
RUN apt-get install -y python3-dev build-essential python3-pip python3-setuptools python3-wheel
RUN pip3 install rdata
RUN pip3 install configargparse

WORKDIR /usr/local/bin
COPY chiron/main.py .
RUN chmod +x main.py

ENTRYPOINT [ "python3", "main.py", "--input", "/input", "--type" , "val", "--output", "/output" ]
