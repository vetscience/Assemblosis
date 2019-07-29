FROM ubuntu:16.04
RUN apt-get update && apt-get install -y wget build-essential cpio less git
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
LABEL about.license="GNU General Public License"
LABEL about.license_file=https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html
RUN conda install recon==1.08
LABEL about.license="GNU General Public License"
RUN conda install repeatscout==1.0.5
RUN conda install -c anaconda perl==5.22.0.1

## Configure RepeatMasker
LABEL about.license="CC0"
LABEL about.license_file="https://creativecommons.org/publicdomain/zero/1.0"
RUN wget http://www.dfam.org/releases/Dfam_3.1/families/Dfam.hmm.gz
#RUN wget http://www.dfam.org/web_download/Release/Dfam_2.0/Dfam.hmm.gz
#COPY Dfam.hmm.gz .
RUN zcat /home/Dfam.hmm.gz > /home/miniconda3/share/RepeatMasker/Libraries/Dfam.hmm && rm -f Dfam.hmm.gz
RUN wget http://www.repeatmasker.org/libraries/RepeatMaskerMetaData-20170127.tar.gz
RUN tar zxf RepeatMaskerMetaData-20170127.tar.gz && rm -f RepeatMaskerMetaData-20170127.tar.gz

# Changes for docker: does not work with udocker
#RUN cp -r /home/miniconda3/pkgs/repeatmasker-4.0.7-pl5.22.0_11/share/RepeatMasker/Libraries /home
#RUN cd /home/miniconda3/pkgs/repeatmasker-4.0.7-pl5.22.0_11/share/RepeatMasker && rm -r Libraries && ln -s$PWD/Libraries

# Install required perl modules
RUN echo -e "yes\ny" > inputJson
RUN perl -MCPAN -e 'install JSON' < inputJson
RUN cpan install LWP::UserAgent

## Install RepeatModeler
LABEL about.license_file=https://opensource.org/licenses/osl-2.1.php
#RUN conda install repeatmodeler==1.0.11
WORKDIR /usr/local
RUN wget http://www.repeatmasker.org/RepeatModeler/RepeatModeler-open-1.0.11.tar.gz
RUN tar zxf RepeatModeler-open-1.0.11.tar.gz && mv RepeatModeler-open-1.0.11 RepeatModeler

# Install files from the assembler
LABEL about.license="BSD 3-Clause License"
WORKDIR /home
RUN git clone --recursive git://github.com/vetscience/Assemblosis
#RUN git clone -b 'v0.1.1-beta' --single-branch --depth 1 https://github.com/vetscience/Assemblosis

WORKDIR /usr/local/RepeatModeler
RUN cp -r /home/Assemblosis/Run/repeatmodeler/RepeatModelerConf/* .
#COPY RepeatModelerConf/RepModelConfig.pm .

WORKDIR /home
RUN cp Assemblosis/Run/repeatmodeler/inputRepeatModeler . && cp Assemblosis/Run/repeatmodeler/inputRepeatMasker .
#COPY inputRepeatMasker .
#COPY inputRepeatModeler .
RUN cp /home/Assemblosis/Run/repeatmodeler/initReps.sh . && cp /home/Assemblosis/Run/repeatmodeler/repeatModeler.sh .
#COPY initReps.sh .
#COPY repeatModeler.sh .
RUN chmod uog+x /home && chmod uog+x initReps.sh && chmod uog+x repeatModeler.sh && chmod uog+x repeatModeler.sh
ENV PATH=$PATH:/usr/local/RepeatMasker:/usr/local/RepeatModeler:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV TERM=xterm
#ENTRYPOINT ["bash","/home/repeatModeler.sh"]
