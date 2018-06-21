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
#echo "Number files in SEARCH PATH with EXTENSION:" $(ls -1 "${SEARCHPATH}"/*."${EXTENSION}" | wc -l)
if [[ -n $1 ]]; then
    echo "Last line of file specified as non-opt/last argument:"
    tail -1 "$1"
fi

# First rename the trimmed reads to enable unique identification
#zcat $TRIMMEDREADS | awk '{print $1""$4}' | sed 's/id=/_read_/1' | gzip > $(echo $TRIMMEDREADS | awk -F"/" '{print "rn_"$NF}')
zcat $TRIMMEDREADS | python /root/renameFasta.py -i - -m mapped.ids | gzip > $(echo $TRIMMEDREADS | awk -F"/" '{print "rn_"$NF}')
