#!/bin/bash

mkdir -p $PWD/Libraries # RepeatMasker.lib will be copied here for masking
cp -rp /home/RepeatMasker $PWD
cp -rp /home/RepeatModeler $PWD

# Changes for docker: does not work with udocker
#cp -r /home/Libraries/* $PWD/Libraries

# This copy circumvents the issue encountered with CWL InitialWorkDir and udocker
#cd /home/miniconda3/pkgs/repeatmasker-4.0.7-pl5.22.0_11/share/RepeatMasker
cd $PWD/RepeatMasker
find /var/lib/cwl -name RMRBSeqs.embl -exec cp {} Libraries \;
perl configure < /home/inputRepeatMasker
#cd /usr/local/RepeatModeler
#perl configure < /home/inputRepeatModeler
