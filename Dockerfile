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
ARG EZ_AF_USER
ARG EZ_AF_PASSWORD
ENV EZ_AF_USER=$EZ_AF_USER
ENV EZ_AF_PASSWORD=$EZ_AF_PASSWORD

# Check for required args
RUN if [ -z $EZ_AF_USER ]; then (printf "\033[1;31mERROR: EZ_AF_USER not included in build args. Include the arg in your build, \n       (e.g: 'docker-compose build --build-arg EZ_AF_USER=\$EZ_AF_USER')\033[0m\n"); exit 1; fi
RUN if [ -z $EZ_AF_PASSWORD ]; then (printf "\033[1;31mERROR: EZ_AF_PASSWORD not included in build args. Include the arg in your build, \n       (e.g: 'docker-compose build --build-arg EZ_AF_PASSWORD=\$EZ_AF_PASSWORD')\033[0m\n"); exit; fi

# Set up the SSH host
RUN apt-get install -y ssh
RUN apt-get install -y sudo
RUN apt-get install -y sshpass

# Create user and password
RUN sudo useradd ${EZ_AF_USER} -m -s /bin/bash
RUN sudo echo "${EZ_AF_USER}:${EZ_AF_PASSWORD}" | sudo chpasswd

# Generate Key
RUN ssh-keygen -N '' -f $HOME/.ssh/id_rsa

# Set up git
RUN apt-get install -y git

# Set wd
WORKDIR /usr/local/airflow
