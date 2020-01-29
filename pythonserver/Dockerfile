FROM python:3.7.6-slim-buster
USER root

# Set up the SSH host
RUN apt-get update
RUN apt-get install -y ssh
RUN apt-get install sudo -y

# Create user and password
RUN sudo useradd -m pythonuser
RUN echo 'pythonuser:pass' | chpasswd

# Add user to ssh
RUN sudo echo 'AllowUsers pythonuser' >> /etc/ssh/sshd_config
RUN sudo echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config

# Install libraries
RUN pip install jupyter jupytext
RUN pip install pandas
