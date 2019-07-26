FROM ubuntu:16.04
RUN apt-get update && apt-get install -y wget bzip2 git
WORKDIR /home

LABEL about.license="BSD 3-clause License"
LABEL about.license_file="https://conda.io/docs/license.html"
LABEL about.license_file="https://repo.continuum.io/EULA/Anaconda+End+User+License+Agreement.txt"
RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN echo -e "\nyes\n" | bash Miniconda3-latest-Linux-x86_64.sh -p /home/miniconda3
ENV PATH=/home/miniconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN conda update -n base conda
RUN conda config --add channels defaults
RUN conda config --add channels conda-forge
RUN conda config --add channels bioconda
LABEL about.license_file=https://opensource.org/licenses/osl-2.1.php
RUN conda install repeatmasker==4.0.7

LABEL about.license="BSD 3-Clause License"
#RUN git clone --recursive git://github.com/vetscience/Assemblosis
RUN git clone -b 'v0.0.3-beta' --single-branch --depth 1 https://github.com/vetscience/Assemblosis
RUN cp Assemblosis/Run/combinecats/combine.sh .
RUN chmod uog+x combine.sh /home
