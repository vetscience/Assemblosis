#!/bin/bash

mkdir -p $PWD/Libraries
cp -rp /home/miniconda3/pkgs/repeatmasker-4.0.7-pl5.22.0_11 $PWD

# Changes for docker: does not work with udocker
#cp -r /home/Libraries/* $PWD/Libraries

# This copy circumvents the issue encountered with CWL InitialWorkDir and udocker
#cd /home/miniconda3/pkgs/repeatmasker-4.0.7-pl5.22.0_11/share/RepeatMasker
cd $PWD/repeatmasker-4.0.7-pl5.22.0_11/share/RepeatMasker
find /var/lib/cwl -name RMRBSeqs.embl -exec cp {} Libraries \;
perl configure < /home/inputRepeatMasker
#cd /usr/local/RepeatModeler
#perl configure < /home/inputRepeatModeler
