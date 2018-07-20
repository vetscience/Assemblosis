#!/bin/bash

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

# NOTE! Assembly is there only to create a step depencendy in CWL workflow
case $key in
    -d|--datadir)
    DATADIR="$2"
    shift # past argument
    shift # past value
    ;;
    -a|--assemblydir)
    ASSEMBLYDIR="$2"
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
    -f|--fofn)
    FOFN="$2"
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
echo ASSEMBLYDIR = "${ASSEMBLYDIR}"
echo ASSEMBLY    = "${ASSEMBLY}"
echo PREFIX      = "${PREFIX}"

# First set up the environment parameters to 4 parallel chunks running all available cpus
cp /root/Assemblosis/preset.xml preset.tmp
NPROC=$((`nproc`/4))
sed "s/NPROC/$NPROC/1" preset.tmp > preset.xml
rm preset.tmp

# Create RW reference data for smrtlink
#rm -rf datasets
#cp -r /root/smrtlink/datasets .
#bash /root/smrtlink/smrtcmds/bin/fasta-to-reference $ASSEMBLY /var/spool/cwl/datasets $PREFIX
echo "fasta-to-reference $ASSEMBLY /root/smrtlink/install/smrtlink-release_5.0.1.9585/bundles/smrttools/install/smrttools-release_5.0.1.9578/private/pacbio/pythonpkgs/pbcore/lib/python2.7/site-packages/pbcore/data/datasets $PREFIX"
#fasta-to-reference $ASSEMBLY /var/spool/cwl/datasets $PREFIX
#fasta-to-reference $ASSEMBLY /root/smrtlink/install/smrtlink-release_5.0.1.9585/bundles/smrttools/install/smrttools-release_5.0.1.9578/private/pacbio/pythonpkgs/pbcore/lib/python2.7/site-packages/pbcore/data/datasets $PREFIX
mkdir -p /root/smrtlink/install/smrtlink-release_5.0.1.9585/bundles/smrttools/install/smrttools-release_5.0.1.9578/private/pacbio/pythonpkgs/pbcore/lib/python2.7/site-packages/pbcore/data/datasets/$PREFIX
mkdir -p /root/smrtlink/install/smrtlink-release_5.0.1.9585/bundles/smrttools/install/smrttools-release_5.0.1.9578/private/pacbio/pythonpkgs/pbcore/lib/python2.7/site-packages/pbcore/data/datasets/$PREFIX/sequence
cp $ASSEMBLY /root/smrtlink/install/smrtlink-release_5.0.1.9585/bundles/smrttools/install/smrttools-release_5.0.1.9578/private/pacbio/pythonpkgs/pbcore/lib/python2.7/site-packages/pbcore/data/datasets/$PREFIX/sequence/$PREFIX.fasta
sawriter /root/smrtlink/install/smrtlink-release_5.0.1.9585/bundles/smrttools/install/smrttools-release_5.0.1.9578/private/pacbio/pythonpkgs/pbcore/lib/python2.7/site-packages/pbcore/data/datasets/$PREFIX/sequence/$PREFIX.fasta.sa /root/smrtlink/install/smrtlink-release_5.0.1.9585/bundles/smrttools/install/smrttools-release_5.0.1.9578/private/pacbio/pythonpkgs/pbcore/lib/python2.7/site-packages/pbcore/data/datasets/$PREFIX/sequence/$PREFIX.fasta -blt 8 -welter
samtools faidx /root/smrtlink/install/smrtlink-release_5.0.1.9585/bundles/smrttools/install/smrttools-release_5.0.1.9578/private/pacbio/pythonpkgs/pbcore/lib/python2.7/site-packages/pbcore/data/datasets/$PREFIX/sequence/$PREFIX.fasta
touch dummy.fastq
ngmlr -r /root/smrtlink/install/smrtlink-release_5.0.1.9585/bundles/smrttools/install/smrttools-release_5.0.1.9578/private/pacbio/pythonpkgs/pbcore/lib/python2.7/site-packages/pbcore/data/datasets/$PREFIX/sequence/$PREFIX.fasta -q dummy.fastq -o dummy.bam -t 1
SEQCNT=`grep ">" $ASSEMBLY | wc -l`
TOTALEN=`grep -v ">" $ASSEMBLY | awk '{c+=length($1)}END{print c}'`
sed "s/ecol/$PREFIX/g;s/>1</>$SEQCNT</1;s/>4670116</>$TOTALEN</1" /root/Assemblosis/referenceset.xml > /root/Assemblosis/referenceset.xml > /root/smrtlink/install/smrtlink-release_5.0.1.9585/bundles/smrttools/install/smrttools-release_5.0.1.9578/private/pacbio/pythonpkgs/pbcore/lib/python2.7/site-packages/pbcore/data/datasets/$PREFIX/referenceset.xml

# Convert hdf5 files to subread format understood by pbsmrtpipe
echo "python /root/Assemblosis/createFofn.py -d $DATADIR -f baxFiles.fofn"
python /root/Assemblosis/createFofn.py -d $DATADIR -f baxFiles.fofn
echo "dataset create --force --type HdfSubreadSet baxFiles.hdfsubreadset.xml baxFiles.fofn"
dataset create --force --type HdfSubreadSet baxFiles.hdfsubreadset.xml baxFiles.fofn
echo "pbsmrtpipe pipeline-id pbsmrtpipe.pipelines.sa3_hdfsubread_to_subread --preset-xml preset.xml -e eid_hdfsubread:baxFiles.hdfsubreadset.xml"
pbsmrtpipe pipeline-id pbsmrtpipe.pipelines.sa3_hdfsubread_to_subread --preset-xml preset.xml -e eid_hdfsubread:baxFiles.hdfsubreadset.xml

# Run arrow
#pbsmrtpipe pipeline-id pbsmrtpipe.pipelines.sa3_ds_resequencing --preset-xml preset.xml -e eid_subread:tasks/pbcoretools.tasks.gather_subreadset-1/file.subreadset.xml -e eid_ref_dataset:/root/smrtlink/install/smrtlink-release_5.0.1.9585/bundles/smrttools/install/smrttools-release_5.0.1.9578/private/pacbio/pythonpkgs/pbcore/lib/python2.7/site-packages/pbcore/data/datasets/$PREFIX/referenceset.xml
echo "pbsmrtpipe pipeline-id pbsmrtpipe.pipelines.sa3_ds_resequencing --preset-xml preset.xml -e eid_subread:tasks/pbcoretools.tasks.gather_subreadset-1/file.subreadset.xml -e eid_ref_dataset:/root/smrtlink/install/smrtlink-release_5.0.1.9585/bundles/smrttools/install/smrttools-release_5.0.1.9578/private/pacbio/pythonpkgs/pbcore/lib/python2.7/site-packages/pbcore/data/datasets/$PREFIX/referenceset.xml"
pbsmrtpipe pipeline-id pbsmrtpipe.pipelines.sa3_ds_resequencing --preset-xml preset.xml -e eid_subread:tasks/pbcoretools.tasks.gather_subreadset-1/file.subreadset.xml -e eid_ref_dataset:/root/smrtlink/install/smrtlink-release_5.0.1.9585/bundles/smrttools/install/smrttools-release_5.0.1.9578/private/pacbio/pythonpkgs/pbcore/lib/python2.7/site-packages/pbcore/data/datasets/$PREFIX/referenceset.xml

# Convert created consensus FASTQ file to a FASTA file
grep -A 1 "^@" tasks/pbcoretools.tasks.gather_fastq-1/file.fastq | sed 's/^@/>/1;s/^\-\-//1;/^$/d' > $PREFIX.contigs.arrowed.fasta
