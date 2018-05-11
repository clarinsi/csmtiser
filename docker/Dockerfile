FROM ubuntu:16.04

RUN apt-get update && apt-get -y install wget python-pip libboost-all-dev git-core build-essential cmake

RUN wget http://www.statmt.org/moses/RELEASE-4.0/binaries/ubuntu-16.04.tgz && \
    tar vxfz ubuntu-16.04.tgz && \
    mv ubuntu-16.04 moses

RUN git clone https://github.com/moses-smt/mgiza.git && \
    cd mgiza/mgizapp && \
    cmake . && \
    make && \
    make install

RUN pip install -r https://raw.githubusercontent.com/clarinsi/csmtiser/master/requirements.txt && \
    cp /mgiza/mgizapp/scripts/merge_alignment.py /mgiza/mgizapp/bin/merge_alignment.py

WORKDIR /csmtiser
