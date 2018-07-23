FROM ubuntu:16.04
RUN apt-get update && apt-get install -y wget unzip samtools rsync
WORKDIR /root

LABEL about.license_file=https://github.com/PacificBiosciences/pbsmrtpipe
LABEL about.license_file=https://github.com/PacificBiosciences/blasr
LABEL about.license_file=https://github.com/PacificBiosciences/GenomicConsensus/blob/develop/LICENSES
LABEL about.license_file=https://support.hdfgroup.org/ftp/HDF5/current/src/unpacked/COPYING
RUN wget https://downloads.pacbcloud.com/public/software/installers/smrtlink_5.0.1.9585.zip
RUN unzip -o -P nX4dmaR% smrtlink_5.0.1.9585.zip
RUN sh smrtlink_5.0.1.9585.run --rootdir smrtlink --smrttools-only
RUN rm -f smrtlink_5.0.1.9585.zip smrtlink_5.0.1.9585.run*
ENV PATH=/root/smrtlink/smrtcmds/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN apt-get update && apt-get install -y git python

LABEL about.license="BSD 3-Clause License"
RUN git clone --recursive git://github.com/vetscience/Assemblosis
#RUN git clone -b 'v0.0.4-beta' --single-branch --depth 1 https://github.com/vetscience/Assemblosis
WORKDIR /root/Assemblosis
RUN chmod uog+x /root && chmod uog+rwx /root/Assemblosis
RUN cp Run/arrow/smrtpipe.sh . && cp Run/arrow/preset.xml . && cp Run/arrow/createFofn.py . && cp Run/arrow/referenceset.xml .
RUN chmod uog+x /root/Assemblosis/createFofn.py && chmod uog+x smrtpipe.sh && chmod uog+x preset.xml
ENV PYTHONPATH=/root/Assemblosis
#RUN mv /root/smrtlink/install/smrtlink-release_5.0.1.9585/bundles/smrttools/install/smrttools-release_5.0.1.9578/private/pacbio/pythonpkgs/pbcore/lib/python2.7/site-packages/pbcore/data/datasets /root/smrtlink/
#RUN ln -s /var/spool/cwl/datasets /root/smrtlink/install/smrtlink-release_5.0.1.9585/bundles/smrttools/install/smrttools-release_5.0.1.9578/private/pacbio/pythonpkgs/pbcore/lib/python2.7/site-packages/pbcore/data/datasets
#ENTRYPOINT ["bash","/root/Assemblosis/smrtpipe.sh"]
