FROM apache/airflow:2.6.0
USER root
# system requirement
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         build-essential \
         git \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# Rust ENV
RUN curl https://sh.rustup.rs -sSf > rustup.sh
RUN chmod 755 rustup.sh
RUN ./rustup.sh -y
RUN rm ./rustup.sh
# Node ENV
RUN curl --silent --location https://deb.nodesource.com/setup_18.x | sudo bash -
RUN apt-get -y update \
  && apt-get install -y --no-install-recommends \
         nodejs \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*