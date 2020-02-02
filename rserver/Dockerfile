FROM rocker/tidyverse:3.6.2

# Install R package dependencies
ADD requirements requirements
RUN Rscript -e "devtools::install_local('requirements')"

# Take in args and set env
ARG EZ_AF_USER
ARG EZ_AF_PASSWORD
ENV EZ_AF_USER=$EZ_AF_USER
ENV EZ_AF_PASSWORD=$EZ_AF_PASSWORD

# Check for args
RUN if [ -z $EZ_AF_USER ]; then (printf "\033[1;31mERROR: EZ_AF_USER not included in build args. Include the arg in your build, \n       (e.g: 'docker-compose build --build-arg EZ_AF_USER=\$EZ_AF_USER')\033[0m\n"); exit 1; fi
RUN if [ -z $EZ_AF_PASSWORD ]; then (printf "\033[1;31mERROR: EZ_AF_PASSWORD not included in build args. Include the arg in your build, \n       (e.g: 'docker-compose build --build-arg EZ_AF_PASSWORD=\$EZ_AF_PASSWORD')\033[0m\n"); exit 1; fi

# Set up the SSH host
RUN apt-get update
RUN apt-get install -y ssh
RUN apt-get install -y sudo
RUN apt-get install -y sshpass

# .R to run during ssh
RUN echo 'rmarkdown::render(commandArgs(trailingOnly = T)[1])' >> /usr/render_rmd.R
RUN sudo chmod a+rwx /usr/render_rmd.R

# Create user and password
RUN sudo useradd ${EZ_AF_USER} -m -s /bin/bash
RUN sudo echo "${EZ_AF_USER}:${EZ_AF_PASSWORD}" | sudo chpasswd

# Add user to ssh
RUN sudo echo "AllowUsers ${EZ_AF_USER}" >> /etc/ssh/sshd_config
RUN sudo echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config

# Expose SSH
EXPOSE 22
