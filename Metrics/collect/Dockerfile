FROM ubuntu:16.04
RUN apt-get update && apt-get install -y python git wget build-essential
WORKDIR /root

LABEL about.license="Artistic License 2.0"
LABEL about.license="MIT License"
RUN wget http://ccb.jhu.edu/software/stringtie/dl/gffread-0.9.12.tar.gz
RUN tar xvfz gffread-0.9.12.tar.gz
WORKDIR /root/gffread-0.9.12
RUN make && mv gffread /usr/local/bin
WORKDIR /root

LABEL about.license="BSD 3-Clause License"
RUN git clone --recursive git://github.com/vetscience/Assemblosis
#RUN git clone -b 'v0.0.3-beta' --single-branch --depth 1 https://github.com/vetscience/Assemblosis
RUN cp /root/Assemblosis/Metrics/collect/*.py .
RUN chmod uog+x /root/*.py /root
#ENTRYPOINT ["python", "/root/createTables.py"]
