############################################################
# Dockerfile to build chiron container
# Based on Ubuntu v23.04
############################################################

FROM ubuntu:23.04
LABEL authors="Richard A. Schäfer"

# update sources list
RUN apt-get -y update && apt-get install -y
RUN apt-get install -y python3-pip python3-dev build-essential python3-configargparse python3-rdata

WORKDIR /usr/local/bin
COPY chiron/main.py .
RUN chmod +x main.py

ENTRYPOINT [ "python3", "main.py" ]
