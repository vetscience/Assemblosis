FROM ubuntu:16.04
# Install dextractor
RUN apt-get update && apt-get install -y git python build-essential parallel libhdf5-dev
WORKDIR /root

LABEL about.license="Copyright (c) 2014, Dr. Eugene W. Myers (EWM). All rights reserved."
LABEL about.license_file=https://github.com/thegenemyers/DEXTRACTOR/blob/master/LICENSE
RUN git clone -b 'V1.0' --single-branch --depth 1 https://github.com/thegenemyers/DEXTRACTOR
WORKDIR DEXTRACTOR
RUN mv Makefile Makefile.orig && sed 1,1d Makefile.orig | sed 's/\/usr\/local\/hdf5/\/usr\/lib\/x86_64-linux-gnu\/hdf5\/serial/1' > Makefile
RUN make && mv dextract /usr/local/bin
WORKDIR /root
RUN rm -rf DEXTRACTOR

LABEL about.license="BSD 3-Clause License"
RUN git clone --recursive git://github.com/vetscience/Assemblosis
#RUN git clone -b 'v0.0.6-beta' --single-branch --depth 1 https://github.com/vetscience/Assemblosis
WORKDIR Assemblosis
RUN chmod uog+x /root && chmod uog+x /root/Assemblosis && chmod uog+x /root/Assemblosis/Run && chmod uog+x /root/Assemblosis/Run/hdf5check && chmod uog+x /root/Assemblosis/Run/hdf5check/hdf5Check.py
ENV PYTHONPATH /root/Assemblosis
#ENTRYPOINT ["python", "/root/Assemblosis/Run/hdf5check/hdf5Check.py"]
