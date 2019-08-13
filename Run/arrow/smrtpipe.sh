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

# First set up the environment parameters to 4 parallel chunks running all available cpus
cp /home/Assemblosis/preset.xml preset.tmp
NPROC=$((`nproc`/4))
mkdir -p $TEMPDIR
sed "s/NPROC/$NPROC/1;s+MYTMPDIR+$TEMPDIR+1" preset.tmp > preset.xml
rm preset.tmp

# Create RW reference data for smrtlink
echo "fasta-to-reference $ASSEMBLY /home/smrtlink/install/smrtlink-release_7.0.1.66975/bundles/smrttools/install/smrttools-release_7.0.1.66768/private/pacbio/pythonpkgs/pbcore/lib/python2.7/site-packages/pbcore/data/datasets $PREFIX"
fasta-to-reference $ASSEMBLY $PWD/datasets $PREFIX

# Convert hdf5 files to subread format understood by pbsmrtpipe
if [ $BAM = "false" ]; then
echo "python /home/Assemblosis/createFofn.py -d $DATADIR -f baxFiles.fofn"
python /home/Assemblosis/createFofn.py -d $DATADIR -f baxFiles.fofn
echo "dataset create --force --type HdfSubreadSet baxFiles.hdfsubreadset.xml baxFiles.fofn"
dataset create --force --type HdfSubreadSet baxFiles.hdfsubreadset.xml baxFiles.fofn
echo "pbsmrtpipe pipeline-id pbsmrtpipe.pipelines.sa3_hdfsubread_to_subread --preset-xml preset.xml -e eid_hdfsubread:baxFiles.hdfsubreadset.xml"
pbsmrtpipe pipeline-id pbsmrtpipe.pipelines.sa3_hdfsubread_to_subread --preset-xml preset.xml -e eid_hdfsubread:baxFiles.hdfsubreadset.xml
echo "pbsmrtpipe pipeline-id pbsmrtpipe.pipelines.sa3_ds_resequencing --preset-xml preset.xml -e eid_subread:tasks/pbcoretools.tasks.gather_subreadset-1/file.subreadset.xml -e eid_ref_dataset:/home/smrtlink/install/smrtlink-release_7.0.1.66975/bundles/smrttools/install/smrttools-release_7.0.1.66768/private/pacbio/pythonpkgs/pbcore/lib/python2.7/site-packages/pbcore/data/datasets/$PREFIX/referenceset.xml"
pbsmrtpipe pipeline-id pbsmrtpipe.pipelines.sa3_ds_resequencing --preset-xml preset.xml -e eid_subread:tasks/pbcoretools.tasks.gather_subreadset-1/file.subreadset.xml -e eid_ref_dataset:$PWD/datasets/$PREFIX/referenceset.xml
else
echo "dataset create --force --type SubreadSet subreadset.xml baxFiles.fofn"
ls $DATADIR/*.bam | while read line; do samtools index $line; done
ls $DATADIR/*.bam | while read line; do pbindex $line; done
dataset create --force --type SubreadSet allTheSubreads.subreadset.xml $DATADIR/*.bam
echo "pbsmrtpipe pipeline-id pbsmrtpipe.pipelines.sa3_ds_resequencing --preset-xml preset.xml -e eid_subread:allTheSubreads.subreadset.xml -e eid_ref_dataset:/home/smrtlink/install/smrtlink-release_7.0.1.66975/bundles/smrttools/install/smrttools-release_7.0.1.66768/private/pacbio/pythonpkgs/pbcore/lib/python2.7/site-packages/pbcore/data/datasets/$PREFIX/referenceset.xml"
pbsmrtpipe pipeline-id pbsmrtpipe.pipelines.sa3_ds_resequencing --preset-xml preset.xml -e eid_subread:allTheSubreads.subreadset.xml -e eid_ref_dataset:$PWD/datasets/$PREFIX/referenceset.xml
fi

# Convert created consensus FASTQ file to a FASTA file
awk '{if (cnt % 4 == 0 || cnt % 4 == 1) print $0; cnt += 1}' tasks/pbcoretools.tasks.gather_fastq-1/file.fastq | sed 's/^@/>/1;s/^\-\-//1;/^$/d' > $PREFIX.contigs.arrowed.fasta

