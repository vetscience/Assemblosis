FROM ubuntu:16.04
RUN apt-get update && apt-get install -y python build-essential perl wget git

LABEL about.license_file=https://www.ncbi.nlm.nih.gov/home/about/policies
WORKDIR /home
RUN wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
RUN tar xvfz taxdump.tar.gz

LABEL about.license="BSD 3-Clause License"
#WORKDIR /home
RUN git clone --recursive git://github.com/vetscience/Assemblosis
#RUN git clone -b 'v0.0.3-beta' --single-branch --depth 1 https://github.com/vetscience/Assemblosis
RUN cp Assemblosis/Run/decon/decon.sh . && cp Assemblosis/Run/decon/taxtreelabel.pl .
RUN cp Assemblosis/Run/decon/mapFasta.py . && cp Assemblosis/Run/decon/fasta.py . && cp Assemblosis/Run/decon/base.py .

RUN chmod uog+x decon.sh && chmod uog+x /home
