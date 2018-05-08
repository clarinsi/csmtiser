FROM ubuntu:16.04

RUN apt update
RUN apt -y upgrade
RUN apt -y install build-essential git-core pkg-config automake libtool wget zlib1g-dev python-dev libbz2-dev
RUN git clone https://github.com/moses-smt/mosesdecoder.git
RUN cd mosesdecoder && make -f contrib/Makefiles/install-dependencies.gmake && ./compile.sh

