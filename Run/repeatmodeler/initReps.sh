#!/bin/bash

mkdir -p /var/spool/cwl/Libraries

# Changes for docker: does not work with udocker
#cp -r /root/Libraries/* /var/spool/cwl/Libraries

# This copy circumvents the issue encountered with CWL InitialWorkDir and udocker
cd /root/miniconda3/pkgs/repeatmasker-4.0.7-pl5.22.0_11/share/RepeatMasker
find /var/lib/cwl -name RMRBSeqs.embl -exec cp {} Libraries \;
perl configure < /root/inputRepeatMasker
#cd /usr/local/RepeatModeler
#perl configure < /root/inputRepeatModeler
