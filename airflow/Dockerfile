FROM jupyter/r-notebook:2023-03-20
USER root

# PSQL Requirements
RUN apt-get update && apt-get install -y libpq-dev build-essential

# Install R dependencies
RUN Rscript -e 'install.packages("ranger", repos = "http://cran.us.r-project.org")'
RUN Rscript -e 'install.packages("RPostgres", repos = "http://cran.us.r-project.org")'
RUN Rscript -e 'install.packages("doParallel", repos = "http://cran.us.r-project.org")'

# Python Requirements
ADD requirements.txt .
RUN pip3 install -r requirements.txt

# Airflow Env Vars
ENV AIRFLOW_HOME='/usr/local/airflow'

# Set wd
WORKDIR /usr/local/airflow

# Sleep forever
CMD sleep infinity
