#!/bin/bash

# Installation script for the assembly pipeline
echo "###########################"
echo "# Starting CWL installation ..."
conda install -c bioconda java-jdk==8.0.112
wget https://github.com/broadinstitute/cromwell/releases/download/44/cromwell-44.jar

echo "###########################"
echo "# Finished CWL installation ..."
