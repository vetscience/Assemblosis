#!/bin/bash

PATH=/home/smrtlink/smrtcmds/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
PYTHONPATH=/home/Assemblosis
cp -r /home/Assemblosis/datasets $PWD

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

# NOTE! Assembly is there only to create a step depencendy in CWL workflow
BAM="false"
case $key in
    -d|--datadir)
    DATADIR="$2"
    shift # past argument
    shift # past value
    ;;
    -t|--tmp)
    TEMPDIR="$2"
    shift # past argument
    shift # past value
    ;;
    -s|--assembly)
    ASSEMBLY="$2"
    shift # past argument
    shift # past value
    ;;
    -p|--prefix)
    PREFIX="$2"
    shift # past argument
    shift # past value
    ;;
    -b|--bam)
    BAM="true"
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

echo DATADIR     = "${DATADIR}"
echo ASSEMBLY    = "${ASSEMBLY}"
echo PREFIX      = "${PREFIX}"
echo BAM         = "${BAM}"
echo TEMPDIR     = "${TEMPDIR}"

NPROC=$((`nproc`))
mkdir -p $TEMPDIR

# Create RW reference data for smrtlink
echo "dataset create --force --type ReferenceSet reference.dataset.xml assembly.fofn"
samtools faidx $ASSEMBLY
sawriter $ASSEMBLY
echo "$ASSEMBLY" > assembly.fofn
dataset create --force --type ReferenceSet reference.dataset.xml assembly.fofn
#dataset create --force --type ReferenceSet $PWD/datasets/reference.dataset.xml assembly.fofn

echo "dataset create --force --type SubreadSet allTheSubreads.subreadset.xml $DATADIR/*.bam"
ls $DATADIR/*.bam | while read line; do samtools index $line; done
ls $DATADIR/*.bam | while read line; do pbindex $line; done
dataset create --force --type SubreadSet allTheSubreads.subreadset.xml $DATADIR/*.bam
echo "pbcromwell run cromwell.workflows.pb_resequencing --overwrite -c 8 --tmp-dir $TEMPDIR -n $NPROC -e eid_subread:allTheSubreads.subreadset.xml -e eid_ref_dataset:reference.dataset.xml"
rm -rf cromwell_out/
pbcromwell run cromwell.workflows.pb_resequencing --overwrite -c 1 --tmp-dir $TEMPDIR -n $NPROC -e eid_subread:allTheSubreads.subreadset.xml -e eid_ref_dataset:reference.dataset.xml

# Convert created consensus FASTQ file to a FASTA file
cp cromwell_out/outputs/consensus.fasta $PREFIX.contigs.arrowed.fasta
#awk '{if (c%4==0||c%4==1) print $0; c+=1}' tasks/pbcoretools.tasks.gather_fastq-1/file.fastq | sed 's/^@/>/1;s/^\-\-//1;/^$/d' > $PREFIX.contigs.arrowed.fasta
#find . -name consensus.fasta -exec ls {} \; | grep genomic_consensus | grep -v "\->" | while read line; do cp $line $PREFIX.contigs.arrowed.fasta; done
