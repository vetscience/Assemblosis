#!/bin/bash
sh /root/initReps.sh
RepeatModeler $@
cp /usr/local/RepeatMasker/Libraries/* /var/spool/cwl/Libraries
