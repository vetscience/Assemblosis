#!/bin/bash

# Installation script for the assembly pipeline
echo "###########################"
echo "# Starting CWL installation ..."
pip install galaxy-lib==18.5.7
conda install -y -c conda-forge nodejs==10.4.1
conda install -y -c conda-forge git==2.18.0
pip install cwltool==1.0.20181012180214

echo "###########################"
echo "# Finished CWL installation ..."
