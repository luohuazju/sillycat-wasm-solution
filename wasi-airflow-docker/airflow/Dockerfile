FROM apache/airflow:2.6.0
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
         git \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
RUN curl https://sh.rustup.rs -sSf > rustup.sh
RUN chmod 755 rustup.sh
RUN ./rustup.sh -y
RUN rm ./rustup.sh