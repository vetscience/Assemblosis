#!/bin/bash

# Installation script for the assembly pipeline
echo "###########################"
echo "# Starting udockertallation ..."
curl https://download.ncg.ingrid.pt/webdav/udocker/udocker-1.1.2.tar.gz > udocker-1.1.2.tar.gz
tar xzvf udocker-1.1.2.tar.gz udocker
./udocker install
mv ./udocker ~/miniconda3/bin/
wget https://github.com/proot-me/proot-static-build/raw/master/static/proot-x86_64 -P ~/miniconda3/bin
wget https://github.com/proot-me/proot-static-build/raw/master/static/proot-x86 -P ~/miniconda3/bin
chmod uog+x ~/miniconda3/bin/proot*

echo "###########################"
echo "# Installing containers ..."
udocker pull pakorhon/arrow:v0.0.7-beta
udocker pull quay.io/biocontainers/bowtie2:2.4.2--py38h1c8e9b9_1
udocker pull quay.io/biocontainers/canu:2.1.1--he1b5a44_0
udocker pull quay.io/biocontainers/centrifuge:1.0.3--py27pl5.22.0_3
udocker pull pakorhon/combinecats:v0.0.4-beta
udocker pull pakorhon/decon:v0.0.5-beta
udocker pull pakorhon/haplomerger:v0.0.7-beta
udocker pull pakorhon/hdf5check:v0.0.6-beta
udocker pull quay.io/biocontainers/repeatmodeler:1.0.11--pl526_1
udocker pull quay.io/biocontainers/pilon:1.23--2
udocker pull pakorhon/renamereads:v0.0.4-beta
udocker pull quay.io/biocontainers/repeatmasker:4.0.9_p2--pl526_2
udocker pull pakorhon/repeatmodeler:v0.0.6-beta
udocker pull quay.io/biocontainers/samtools:1.11--h6270b1f_0
udocker pull quay.io/biocontainers/trimmomatic:0.39--1

echo "###########################"
echo "# Finished udocker installation ..."
