#!/bin/bash
sh /home/initReps.sh
cp $PWD/RepeatMasker/Libraries/RepeatMasker.lib $PWD/Libraries
export PERL5LIB=$PWD/RepeatMasker:$PWD/RepeatModeler
RepeatModeler $@
