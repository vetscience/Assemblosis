#!/bin/bash
sh /home/initReps.sh
cp /home/RepeatMasker/Libraries/RepeatMasker.lib $PWD/Libraries
RepeatModeler $@
