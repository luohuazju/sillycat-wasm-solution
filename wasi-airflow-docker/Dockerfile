FROM apache/airflow:2.6.0
USER root

# system requirement on top of 
# airflow 2.6.0 based on python:3.7-slim-bullseye
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         build-essential \
         git \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Rust ENV to enable our cargo
RUN curl https://sh.rustup.rs -sSf > rustup.sh \
  && chmod 755 rustup.sh \
  && ./rustup.sh -y \
  && rm ./rustup.sh

# Node ENV to enable our ActionScript
RUN curl --silent --location https://deb.nodesource.com/setup_18.x | sudo bash -
RUN apt-get -y update \
  && apt-get install -y --no-install-recommends \
         nodejs \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

#set up the app
EXPOSE  8080
RUN     mkdir -p /app/ 
ADD     start.sh /app/ 
WORKDIR /app/
CMD	[ "./start.sh" ]