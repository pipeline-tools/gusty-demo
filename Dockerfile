FROM python:3.7.6-slim-buster
USER root

# PSQL Requirements
RUN apt-get update && apt-get install -y libpq-dev build-essential

# Requirements
ADD requirements.txt .
RUN pip install -r requirements.txt

# Airflow Env Vars
ENV AIRFLOW_HOME='/usr/local/airflow'

# Take in args and set env
ARG GUSTY_USER
ARG GUSTY_PASSWORD
ENV GUSTY_USER=$GUSTY_USER
ENV GUSTY_PASSWORD=$GUSTY_PASSWORD

# Check for required args
RUN if [ -z $GUSTY_USER ]; then (printf "\033[1;31mERROR: GUSTY_USER not included in build args. Include the arg in your build, \n       (e.g: 'docker-compose build --build-arg GUSTY_USER=\$GUSTY_USER')\033[0m\n"); exit 1; fi
RUN if [ -z $GUSTY_PASSWORD ]; then (printf "\033[1;31mERROR: GUSTY_PASSWORD not included in build args. Include the arg in your build, \n       (e.g: 'docker-compose build --build-arg GUSTY_PASSWORD=\$GUSTY_PASSWORD')\033[0m\n"); exit; fi

# Set up the SSH host
RUN apt-get update --fix-missing
RUN apt-get install -y sudo
RUN apt-get install -y ssh
RUN apt-get install -y sshpass

# Create user and password
RUN sudo useradd ${GUSTY_USER} -m -s /bin/bash
RUN sudo echo "${GUSTY_USER}:${GUSTY_PASSWORD}" | sudo chpasswd

# Generate Key
RUN ssh-keygen -N '' -f $HOME/.ssh/id_rsa

# Set up git
RUN apt-get install -y git

# Set wd
WORKDIR /usr/local/airflow
