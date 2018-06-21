#!/bin/bash                                                                                                                  
POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

# NOTE! Assembly option is there only to create a step depencendy in CWL workflow
case $key in
    -a|--assembly)
    ASSEMBLY="$2"
    shift # past argument
    shift # past value
    ;;
    -c|--cats)
    CATFILES="$2"
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

WORKDIR="RepeatResults"
echo WORKDIR = "${WORKDIR}"
echo ASSEMBLY = "${ASSEMBLY}"
echo CATFILES = "${CATFILES}"

mkdir -p $WORKDIR
cp $ASSEMBLY $WORKDIR
touch $WORKDIR/all.cat
for catFile in ${CATFILES//,/ };
do
if [[ $catFile = *".gz" ]]; then
zcat $catFile >> $WORKDIR/all.cat
else
cat $catFile >> $WORKDIR/all.cat
fi
done
gzip -f $WORKDIR/all.cat
ProcessRepeats -maskSource ${WORKDIR}/$(basename $ASSEMBLY) -u -gff -xsmall ${WORKDIR}/all.cat.gz
