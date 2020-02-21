FROM python:3.7.6-slim-buster
USER root

# PSQL Requirements
#RUN apt-get update && apt-get install -y libpq-dev build-essential

# Take in args and set env
ARG GUSTY_USER
ARG GUSTY_PASSWORD
ENV GUSTY_USER=$GUSTY_USER
ENV GUSTY_PASSWORD=$GUSTY_PASSWORD

# Check for args
RUN if [ -z $GUSTY_USER ]; then (printf "\033[1;31mERROR: GUSTY_USER not included in build args. Include the arg in your build, \n       (e.g: 'docker-compose build --build-arg GUSTY_USER=\$GUSTY_USER')\033[0m\n"); exit 1; fi
RUN if [ -z $GUSTY_PASSWORD ]; then (printf "\033[1;31mERROR: GUSTY_PASSWORD not included in build args. Include the arg in your build, \n       (e.g: 'docker-compose build --build-arg GUSTY_PASSWORD=\$GUSTY_PASSWORD')\033[0m\n"); exit 1; fi

# Set up the SSH host
RUN apt-get update
RUN apt-get install -y ssh
RUN apt-get install -y sudo
RUN apt-get install -y sshpass

# Create user and password
RUN sudo useradd ${GUSTY_USER} -m -s /bin/bash
RUN sudo echo "${GUSTY_USER}:${GUSTY_PASSWORD}" | sudo chpasswd

# Add user to ssh
RUN sudo echo "AllowUsers ${GUSTY_USER}" >> /etc/ssh/sshd_config
RUN sudo echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config

# Install libraries
RUN pip install jupyter
RUN pip install jupytext
RUN pip install pandas
#RUN pip install siuba

# Expose SSH
EXPOSE 22
