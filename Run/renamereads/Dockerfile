FROM ubuntu:16.04
RUN apt-get update && apt-get install -y python git
WORKDIR /home

LABEL about.license="BSD 3-Clause License"
RUN git clone --recursive git://github.com/vetscience/Assemblosis
#RUN git clone -b 'v0.0.3-beta' --single-branch --depth 1 https://github.com/vetscience/Assemblosis
RUN cp Assemblosis/Run/renamereads/base.py . && cp Assemblosis/Run/renamereads/renameFasta.py . && cp Assemblosis/Run/renamereads/renamereads.sh .
RUN chmod uog+x renamereads.sh /home
