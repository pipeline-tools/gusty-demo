FROM rocker/tidyverse:3.6.2

# Set up the SSH host
RUN apt-get update
RUN apt-get install -y ssh
RUN echo "service ssh start" >> /etc/cont-init.d/userconf

# Install R package dependencies
ADD requirements requirements
RUN Rscript -e "devtools::install_local('requirements')"
