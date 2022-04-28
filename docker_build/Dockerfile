FROM ubuntu:20.04
LABEL maintainer="datafuel"

# Never prompt the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

# OS Deps

RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        freetds-bin \
        software-properties-common \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        gcc \
        python3.8-dev \
        curl \
        rsync \
        netcat \
        locales \
        unixodbc-dev \
        python3-pip \
        alien
        
RUN cd "$(dirname $(which python3))" \
    && ln -s python3 python \
    && pip install -U pip setuptools wheel
    # && pip install -U pip setuptools wheel \
    # && ln -s pip3 pip

## Install Dremio ODBC Driver
WORKDIR /drivers
RUN curl -L https://download.dremio.com/odbc-driver/dremio-odbc-LATEST.x86_64.rpm --output dremio-odbc-LATEST.x86_64.rpm \
    && alien -i dremio-odbc-LATEST.x86_64.rpm

# Set the working directory in the image/container to /src
WORKDIR /src

# Copy & Install the python dependencies 
COPY requirements.txt .
RUN pip install -r requirements.txt

# Add /src to PYTHONPATH
ENV PYTHONPATH "$PYTHONPATH:/src:"
ENV PATH "$PATH:/src:/drivers"