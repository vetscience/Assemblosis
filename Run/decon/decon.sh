#!/bin/bash

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -U|--trimmed-reads)
    TRIMMEDREADS="$2"
    shift # past argument
    shift # past value
    ;;
    -S|--classification-file)
    CLASSIFICATION="$2"
    shift # past argument
    shift # past value
    ;;
    -t|--taxons)
    TAXONS="$2"
    shift # past argument
    shift # past value
    ;;
    -m|--mapped-ids)
    MAPPEDIDS="$2"
    shift # past argument
    shift # past value
    ;;
    -p|--partial-match-len)
    PARTIALMATCH="$2"
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
echo CLASSIFICATION = "${CLASSIFICATION}"
echo TAXONS         = "${TAXONS}"
echo MAPPEDIDS      = "${MAPPEDIDS}"
echo PARTIALMATCH      = "${PARTIALMATCH}"

if [[ -n $1 ]]; then
    echo "Last line of file specified as non-opt/last argument:"
    tail -1 "$1"
fi

# First rename the trimmed reads to enable unique identification
awk -v var="$PARTIALMATCH" 'NR>1{if ($6>=PARTIALMATCH) print $0"\t"$3}' $CLASSIFICATION > classification.converted
touch taxon.ids
for taxon in  ${TAXONS//,/ };
do
perl /root/taxtreelabel.pl classification.converted $taxon && awk '{print $1}' in_tree.txt | sort | uniq >> taxon.ids
done
sort taxon.ids | uniq > contaminated.read.ids.unique

zcat $TRIMMEDREADS > trimmed.fasta
grep ">" trimmed.fasta | sed 's/>//1' > trimmedReads.ids
fgrep -w -f contaminated.read.ids.unique trimmedReads.ids > contaminated.read.ids.orig
fgrep -v -w -f contaminated.read.ids.orig trimmedReads.ids > trimmedReads.ids.decon

python /root/mapFasta.py -i trimmed.fasta -s contaminated.read.ids.unique -m $MAPPEDIDS -r | gzip > contaminatedReads.fa.gz
python /root/mapFasta.py -i trimmed.fasta -s trimmedReads.ids.decon -m $MAPPEDIDS -r | gzip > trimmedReads.decon.fa.gz
