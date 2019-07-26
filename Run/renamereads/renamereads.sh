#!/bin/bash

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

# NOTE! Assembly is there only to create a step depencendy in CWL workflow
case $key in
    -U|--trimmed-reads)
    TRIMMEDREADS="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

echo TRIMMEDREADS   = "${TRIMMEDREADS}"

# First rename the trimmed reads to enable unique identification
zcat $TRIMMEDREADS | python /home/renameFasta.py -i - -m mapped.ids | gzip > $(echo $TRIMMEDREADS | awk -F"/" '{print "rn_"$NF}')
