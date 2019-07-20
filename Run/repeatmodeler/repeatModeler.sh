#!/bin/bash
sh /root/initReps.sh
cp /root/miniconda3/pkgs/repeatmasker-4.0.7-pl5.22.0_11/share/RepeatMasker/Libraries/RepeatMasker.lib $HOME/Libraries
RepeatModeler $@
