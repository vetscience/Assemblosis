FROM ubuntu:16.04
RUN apt-get update && apt-get install -y python perl wget git
WORKDIR /root
RUN git clone -b 'v0.0.1-beta' --single-branch --depth 1 https://github.com/vetscience/Assemblosis
RUN cp Assemblosis/Run/decon/decon.sh . && cp Assemblosis/Run/decon/taxtreelabel.pl .
RUN cp Assemblosis/Run/decon/mapFasta.py . && cp Assemblosis/Run/decon/fasta.py . && cp Assemblosis/Run/decon/base.py .
RUN wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
RUN tar xvfz taxdump.tar.gz
#RUN gzip names.dmp && gzip nodes.dmp
RUN chmod uog+x decon.sh && chmod uog+x /root
ENTRYPOINT ["/root/decon.sh"]
