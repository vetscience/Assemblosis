FROM ubuntu:16.04
RUN apt-get update && apt-get install -y wget perl python parallel git
WORKDIR /home

LABEL about.license_file=file:///C:/Users/pkorhonen/Downloads/manual.v3.6%20(1).pdf
RUN wget https://github.com/mapleforest/HaploMerger2/releases/download/HaploMerger2_20161205/HaploMerger2_20161205.tar.gz
RUN tar xvfz HaploMerger2_20161205.tar.gz

LABEL about.license="BSD 3-Clause License"
RUN git clone --recursive git://github.com/vetscience/Assemblosis
#RUN git clone -b 'v0.1.1-beta' --single-branch --depth 1 https://github.com/vetscience/Assemblosis
RUN cp Assemblosis/Run/haplomerger/base.py . && cp Assemblosis/Run/haplomerger/fasta.py . && cp Assemblosis/Run/haplomerger/haploMerger.py . && cp Assemblosis/Run/haplomerger/haploMerger.sh .
ENV HAPLOMERGER_DIR=/home/HaploMerger2_20161205
ENV PATH=/home/HaploMerger2_20161205/lastz_1.02.00_unbuntu64bit:/home/HaploMerger2_20161205/chainNet_jksrc20100603_ubuntu64bit:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN chmod uog+x /home && chmod uog+x /home/haploMerger.py && chmod uog+x /home/haploMerger.sh

