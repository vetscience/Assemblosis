FROM ubuntu:16.04
# Install dextractor
RUN apt-get update && apt-get install -y git python2.7 build-essential wget parallel libhdf5-dev
WORKDIR /root

LABEL about.license="Copyright (c) 2014, Dr. Eugene W. Myers (EWM). All rights reserved."
LABEL about.license_file=https://github.com/thegenemyers/DEXTRACTOR/blob/master/LICENSE
RUN git clone -b 'V1.0' --single-branch --depth 1 https://github.com/thegenemyers/DEXTRACTOR
WORKDIR DEXTRACTOR
RUN mv Makefile Makefile.orig && sed 1,1d Makefile.orig | sed 's/\/usr\/local\/hdf5/\/usr\/lib\/x86_64-linux-gnu\/hdf5\/serial/1' > Makefile
RUN make && mv dextract /usr/bin
WORKDIR /root
RUN rm -rf DEXTRACTOR

LABEL about.license="BSD 3-clause License"
LABEL about.license_file="https://conda.io/docs/license.html"
LABEL about.license_file="https://repo.continuum.io/EULA/Anaconda+End+User+License+Agreement.txt"
RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN echo -e "\nyes\n" | bash Miniconda3-latest-Linux-x86_64.sh
ENV PATH=/root/miniconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN conda update -n base conda
RUN conda config --add channels defaults
RUN conda config --add channels conda-forge
RUN conda config --add channels bioconda
LABEL about.license_file=https://opensource.org/licenses/osl-2.1.php
RUN conda install bedtools==2.27.1

LABEL about.license="BSD 3-Clause License"
RUN git clone --recursive git://github.com/vetscience/Assemblosis
#RUN git clone -b 'v0.1.0-beta' --single-branch --depth 1 https://github.com/vetscience/Assemblosis
WORKDIR Assemblosis
RUN chmod uog+x /root && chmod uog+x /root/Assemblosis && chmod uog+x /root/Assemblosis/Run && chmod uog+x /root/Assemblosis/Run/hdf5check && chmod uog+x /root/Assemblosis/Run/hdf5check/hdf5Check.py
ENV PYTHONPATH /root/Assemblosis
#ENTRYPOINT ["python", "/root/Assemblosis/Run/hdf5check/hdf5Check.py"]
