#!/bin/bash
sh /home/initReps.sh
cp /home/miniconda3/pkgs/repeatmasker-4.0.7-pl5.22.0_11/share/RepeatMasker/Libraries/RepeatMasker.lib $PWD/Libraries
RepeatModeler $@
