## CWL based workflow to assemble haploid/diploid eukaryote genomes of non-model organisms
The workflow is designed to use both PacBio long-reads and Illumina short-reads. The workflow first extracts, corrects, trims and decontaminates the long reads. Decontaminated trimmed reads are then used to assemble the genome and raw reads are used to polish it. Next, Illumina reads are cleaned and used to further polish the resultant assembly. Finally, the polished assembly is masked using inferred repeats and haplotypes are eliminated. The workflow uses BioConda and DockerHub to install required software and is therefore fully automated. In addition to final assembly, the workflow produces intermediate assemblies before and after polishing steps. The workflow follows the syntax for CWL v1.0.

### Dependencies
Programs
* [udocker v1.1.1](https://github.com/indigo-dc/udocker)
* [cwltool v1.0.20180403145700](https://github.com/common-workflow-language/cwltool)
* [nodejs v10.4.1 required by cwltool](https://nodejs.org/en)
* [Python library galaxy-lib v18.5.7](https://pypi.org/project/galaxy-lib)

Data
* [Illumina adapters converted to FASTA format](http://sapac.support.illumina.com/downloads/illumina-adapter-sequences-document-1000000002694.html)
* [NCBI nucleotide non-redundant sequences for decontamination with Centrifuge](http://www.ccb.jhu.edu/software/centrifuge)
* [RepBase v17.02 file RMRBSeqs.embl](https://www.girinst.org/repbase)

### Installation
Install udocker from [BioConda: udocker v1.1.1](https://bioconda.github.io/recipes/udocker/README.html). For instance:
```
cd
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
echo -e "\nyes\n\nyes\n" | bash Miniconda3-latest-Linux-x86_64.sh
export PATH=~/miniconda3/bin:$PATH
conda update -n base conda
conda config --add channels defaults
conda config --add channels conda-forge
conda config --add channels bioconda
conda install -p ~/miniconda3 udocker==1.1.1
```
Add following line to 2nd line of udocker script (~/miniconda3/bin/udocker):
```
2c2
< export CONDA_PREFIX=~/miniconda3
---
>
```
Note that udocker may require fairly recent Linux distribution: [https://indigo-dc.gitbooks.io/udocker/content/doc/user_manual.html](https://indigo-dc.gitbooks.io/udocker/content/doc/user_manual.html).

Follow installation guidelines given for the programs cwltool, galaxy-lib, nodejs and git in their web-sites or use pip and conda:
```
pip install galaxy-lib==18.5.7
conda install -c conda-forge nodejs==10.4.1
pip install cwltool==v1.0.20180403145700
conda install -c conda-forge git==2.18.0
```

For cwltool, apply following fix in the file ~/miniconda3/lib/python2.7/site-packages/cwltool/job.py
```
471,473c471,472
<         if env != None: # This is the fix
<             for key in env:
<                 env_copy[key] = env[key]
---
>         for key in env:
>             env_copy[key] = env[key]
```

Download and extract RepBase database, Centrifuge version of NCBI nt database and create Illumina adapter FASTA file to your preferred locations.
The location of these data will be defined in the configuration (.yml) file.

### Usage
You have to create a YAML (.yml) file for each assembly. This file defines the required parameters and the location for both PacBio and Illumina raw-reads.
```
> cd
> git clone -b 'v0.0.6-beta' --single-branch --depth 1 https://github.com/vetscience/Assemblosis
> cd Assemblosis/Run
> cp ../Examples/assemblyCele.yml .

"Edit assemblyCele.yml to fit your computing environment and to define the location for the read files, databases and Illumina adapters"

> mkdir RepeatSimple; mkdir RepeatTransp; mkdir RepeatCustom
> cwltool --tmpdir-prefix /home/<username>/Tmp --cachedir /home/<username>/Cache --user-space-docker-cmd udocker --leave-tmpdir assembly.cwl assemblyCele.yml
```

An annotated example of the YAML file for Caenorhabditis elegans assembly.
```
## Top level directory, which contains the PacBio raw data
# NOTE! The software looks for all .h5 files recursively in given directory
pacBioDataDir:
  class: Directory
  location: /home/<username>/Dna

## Prefix for the resultant assembly files
prefix: cele

## Maximum number of threads used in the pipeline
threads: 24

## Expected genome size. This parameter is forwarded to Canu assembler.
genomeSize: 100m 

## Minimum length for the PacBio reads used for the assembly. This parameter is forwarded to Canu assembler.
# The maximum resolvable repeat regions becomes 2 x minReadLength
minReadLen: 6000 

## Parameter for Canu assembler to adjust to GC-content. Should be 0.15 for high or low GC content.
corMaxEvidenceErate: 0.20  

## Paired-end (PE) reads of Illumina raw data. These files are given to the program Trimmomatic.
# NOTE! Two pairs given below.
readsPe1:
  - class: File
    format: edam:format_1930  # fastq
    path: /home/<username>/Dna/SRR2598966_1.fastq.gz
  - class: File
    format: edam:format_1930  # fastq
    path: /home/<username>/Dna/SRR2598967_1.fastq.gz
readsPe2:
  - class: File
    format: edam:format_1930  # fastq
    path: /home/<username>/Dna/SRR2598966_2.fastq.gz
  - class: File
    format: edam:format_1930  # fastq
    path: /home/<username>/Dna/SRR2598967_2.fastq.gz

## Phred coding of Illumina data. This parameter is forwarded to Trimmomatic.
# NOTE! Each read-pair needs one phred value.
phredsPe: ['33','33']

## Sliding window and illuminaClip parameters for Trimmomatic
slidingWindow:
    windowSize: 4
    requiredQuality: 25
illuminaClip:
    adapters:
        class: File
        path: <path to Illumina adapter file>
    seedMismatches: 2
    palindromeClipThreshold: 30
    simpleClipThreshold: 10
    minAdapterLength: 20
    keepBothReads: true
## Further parameters for Trimmomatic
# Required phred-quality for leading 5 nucleotides
leading: 25
# Required phred-quality for trailing 5 nucleotides
trailing: 25
# Minimum accepted read-length to keep the read after trimming
minlen: 40

## Illumina PE fragment length. This parameter is forwarded to bowtie2 mapper.
# NOTE! Each read-pair needs one phred value.
maxFragmentLens: [500, 600]

## Parameters for the program Pilon
# Orientation of pair-end reads e.g. 'fr', 'rf', 'ff'
orientation: 'fr'
# Prefix for the resultant pilon polished assembly
polishedAssembly: celePilon 
# This is set 'true' for an organism with diploid genome: Pilon parameter --diploid
diploidOrganism: true
# Value 'bases' fixes snps and indels: pilon parameter --fix
fix: bases

## Parameters for the program Centrifuge.
# Path to the directory, that contains NCBI nt database in nt.?.cf files.
database: /home/<username>/ntDatabase
# NCBI taxon root identifers for the species considered contaminants: e.g. bacteria (=2), viruses (=10239), fungi (=4751), mammals (=40674), artificial seqs (=81077).
taxons: [2,10239,4751,40674,81077]
# Lenght of the identical match in nucleotides required to infer a read as contaminant.
partialMatch: 100

## Parameters for the RepeatModeler and RepeatMasker
repBaseLibrary:
  class: File
  # This is the RepBase file from https://www.girinst.org/repbase
  path: /home/<username>/RepBaseLibrary/RMRBSeqs.embl
# Directories for inferred custom repeats (inferred by RepeatModeler), tandem repeats (simple repeats) and interspersed repeats (transposons)
repeatWorkDir:
  - class: Directory
    location: RepeatCustom
  - class: Directory
    location: RepeatSimple
  - class: Directory
    location: RepeatTransp
# Represents -noint parameter for masking custom, tandem and interspersed repeats
noInterspersed: [false, true, false]
# Represents -nolow parameter for masking custom, tandem and interspersed repeats
noLowComplexity: [true, false, true]
```
### Runtimes and hardware requirements
The workflow was tested in Linux environment (CentOS Linux release 7.2.1511) in a server with 24 physical CPUs (48 hyperthreaded CPUs) and 512 GB RAM.
Runtimes for the assemblies of *Caenorhabditis elegans*, *Drosophila melanogaster* and *Plasmodium falciparum* were 1537, 6501 and 424 CPU hours, respectively.
Maximum memory usage of 134.1 GB was claimed by the program Centrifuge for each assembly.

### Software tools used in this pipeline
* [Dextractor v1.0](https://github.com/thegenemyers/DEXTRACTOR)
* [Trimmomatic v0.36](http://www.usadellab.org/cms/?page=trimmomatic)
* [Centrifuge v1.0.3](http://www.ccb.jhu.edu/software/centrifuge)
* [Canu v1.6](http://canu.readthedocs.io/en/latest/index.html)
* [Arrow in SmrtLink v5.0.1](https://www.pacb.com/support/software-downloads)
* [Bowtie 2 v2.2.8](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml)
* [SAMtools v1.6](http://samtools.sourceforge.net)
* [Pilon v1.22](https://github.com/broadinstitute/pilon)
* [RepeatMasker v4.0.6](http://www.repeatmasker.org)
* [RepeatModeler v1.0.11](http://www.repeatmasker.org)
* [RepBase v17.02](https://www.girinst.org/repbase)
* [HaploMerger2 build_20160512](https://github.com/mapleforest/HaploMerger2)

### Cite
If you use the pipeline, please cite: TBD

