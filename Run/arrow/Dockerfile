FROM ubuntu:16.04
RUN apt-get update && apt-get install -y wget unzip samtools rsync
WORKDIR /home

LABEL about.license_file=https://github.com/PacificBiosciences/pbsmrtpipe
LABEL about.license_file=https://github.com/PacificBiosciences/blasr
LABEL about.license_file=https://github.com/PacificBiosciences/GenomicConsensus/blob/develop/LICENSES
LABEL about.license_file=https://support.hdfgroup.org/ftp/HDF5/current/src/unpacked/COPYING
RUN wget https://downloads.pacbcloud.com/public/software/installers/smrtlink_9.0.0.92188.zip
#RUN unzip -o -P 9rVkq3HT smrtlink_9.0.0.92188.zip
RUN unzip -o smrtlink_9.0.0.92188.zip
RUN sh smrtlink_9.0.0.92188.run --rootdir smrtlink --smrttools-only
RUN rm -f smrtlink_9.0.0.92188.zip smrtlink_9.0.0.92188.run*
ENV PATH=/home/smrtlink/smrtcmds/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN apt-get update && apt-get install -y git python

LABEL about.license="BSD 3-Clause License"
WORKDIR /home
#RUN git clone --recursive git://github.com/vetscience/Assemblosis
#RUN git clone -b 'v0.1.2-beta' --single-branch --depth 1 https://github.com/vetscience/Assemblosis
#WORKDIR /home/Assemblosis
#RUN chmod uog+rx /home && chmod uog+rwx /home/Assemblosis
#RUN cp Run/arrow/smrtpipe.sh . && cp Run/arrow/preset.xml . && cp Run/arrow/createFofn.py . && cp Run/arrow/referenceset.xml .
#RUN chmod uog+x /home/Assemblosis/createFofn.py && chmod uog+x smrtpipe.sh && chmod uog+x preset.xml
RUN mkdir -p datasets && cp -r /home/smrtlink/install/smrtlink-release_9.0.0.92188/bundles/smrttools/install/smrttools-release_9.0.0.92188/private/pacbio/python3pkgs/pbcore-py3/lib/python3.7/site-packages/pbcore/data/datasets/* datasets
RUN chmod -R uog+rx datasets && rm -r /home/smrtlink/install/smrtlink-release_9.0.0.92188/bundles/smrttools/install/smrttools-release_9.0.0.92188/private/pacbio/python3pkgs/pbcore-py3/lib/python3.7/site-packages/pbcore/data/datasets
RUN ln -s $HOME/datasets /home/smrtlink/install/smrtlink-release_9.0.0.92188/bundles/smrttools/install/smrttools-release_9.0.0.92188/private/pacbio/python3pkgs/pbcore-py3/lib/python3.7/site-packages/pbcore/data/datasets
#ENV PYTHONPATH=/home/Assemblosis
ENV PYTHONPATH=/home
COPY smrtpipe.sh .
