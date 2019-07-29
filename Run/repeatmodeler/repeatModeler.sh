#!/bin/bash
sh /home/initReps.sh
cp $PWD/RepeatMasker/Libraries/RepeatMasker.lib $PWD/Libraries
RepeatModeler $@
