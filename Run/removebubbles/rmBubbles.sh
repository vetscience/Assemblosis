#!/bin/bash                                                                                                                  
POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -a|--assembly)
    ASSEMBLY="$1"
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

echo ASSEMBLY = "${ASSEMBLY}"
awk '{if (($0~/^>/) && ($0~/suggestBubble=no/)) s=1; else if ($0~/^>/) s=0; if (s==1) print $0;}' ${ASSEMBLY} > filtered.${ASSEMBLY}
