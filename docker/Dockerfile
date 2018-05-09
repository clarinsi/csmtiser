FROM ubuntu:16.04

RUN apt-get update && apt-get -y install wget

RUN wget http://www.statmt.org/moses/RELEASE-4.0/binaries/ubuntu-16.04.tgz
RUN tar vxfz ubuntu-16.04.tgz
RUN mv ubuntu-16.04 moses

RUN apt-get -y install libboost-all-dev git-core
RUN apt-get -y install build-essential cmake
RUN git clone https://github.com/moses-smt/mgiza.git && \
    cd mgiza/mgizapp && \
    cmake . && \
    make && \
    make install

RUN git clone https://github.com/clarinsi/csmtiser.git
RUN apt-get -y install python-pip
RUN pip install -r /csmtiser/requirements.txt
RUN cp /mgiza/mgizapp/scripts/merge_alignment.py /mgiza/mgizapp/bin/merge_alignment.py
