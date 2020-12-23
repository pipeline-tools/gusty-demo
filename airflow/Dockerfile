FROM python:3.9.1-slim-buster
USER root

# PSQL Requirements
RUN apt-get update && apt-get install -y libpq-dev build-essential

# Get R
RUN apt-get -y install libssl-dev libgit2-dev libcurl4-gnutls-dev libxml2-dev openssl
RUN apt-get -y install dirmngr --install-recommends
RUN apt-get -y install software-properties-common
RUN apt-get -y install apt-transport-https
RUN apt-key adv --keyserver keys.gnupg.net --recv-key 'E19F5F87128899B192B1A2C2AD5F960A256A04AF'
RUN add-apt-repository 'deb http://cloud.r-project.org/bin/linux/debian buster-cran40/'
RUN apt-get update
RUN apt-get -y install r-base

# Install R dependencies
RUN Rscript -e 'install.packages("devtools")'
RUN Rscript -e 'install.packages("tidyverse")'
RUN Rscript -e 'install.packages("doParallel")'
RUN Rscript -e 'install.packages("tidymodels")'
RUN Rscript -e 'install.packages("ranger")'
RUN Rscript -e 'install.packages("RPostgres")'

# Python Requirements
ADD requirements.txt .
RUN pip3 install -r requirements.txt

# Airflow Env Vars
ENV AIRFLOW_HOME='/usr/local/airflow'

# Set wd
WORKDIR /usr/local/airflow

# Sleep forever
CMD sleep infinity
