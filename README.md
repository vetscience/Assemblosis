## CWL based workflow to assemble haploid/diploid eukaryote genomes of non-model organisms
The workflow is designed to use both PacBio long-reads and Illumina short-reads. The workflow first extracts, corrects, trims and decontaminates the long reads. Decontaminated trimmed reads are then used to assemble the genome and raw reads are used to polish it. Next, Illumina reads are cleaned and used to further polish the resultant assembly. Finally, the polished assembly is masked using inferred repeats and haplotypes are eliminated. The workflow uses BioConda and DockerHub to install required software and is therefore fully automated. In addition to final assembly, the workflow produces intermediate assemblies before and after polishing steps. The workflow follows the syntax for CWL v1.0.

### Dependencies
Programs
* [udocker v1.1.1](https://github.com/indigo-dc/udocker)
* [udocker snapshot](https://raw.githubusercontent.com/indigo-dc/udocker/7f6975c19c63c3d65ec6256c7cf5b2369d5c115d/udocker.py)
* [cwltool v1.0.20180403145700](https://github.com/common-workflow-language/cwltool)
* [nodejs v10.4.1 required by cwltool](https://nodejs.org/en)
* [Python library galaxy-lib v18.5.7](https://pypi.org/project/galaxy-lib)

Data
* [Illumina adapters converted to FASTA format](http://sapac.support.illumina.com/downloads/illumina-adapter-sequences-document-1000000002694.html)
* [NCBI nucleotide non-redundant sequences for decontamination with Centrifuge](http://www.ccb.jhu.edu/software/centrifuge)
* [RepBase v17.02 file RMRBSeqs.embl](https://www.girinst.org/repbase)

### Installation
Use installation script ```install.sh``` to install program dependencies.
```
# First confirm that you have the program 'git' installed in your system
cd
git clone -b 'v0.0.3-publication' --single-branch --depth 1 https://github.com/vetscience/Assemblosis
cd Assemblosis
bash install.sh

```
For data dependencies: download and extract [RepBase database](https://www.girinst.org/repbase), download Centrifuge version of [NCBI nt database](http://www.ccb.jhu.edu/software/centrifuge) and create [Illumina adapter FASTA file](http://sapac.support.illumina.com/downloads/illumina-adapter-sequences-document-1000000002694.html) to your preferred locations. If your reads are clean from adapters, the adapter FASTA file can be empty.
Give the location of these data in the configuration (.yml) file (see **Usage**).

### Usage
You have to create a YAML (.yml) file for each assembly. This file defines the required parameters and the location for both PacBio and Illumina raw-reads.
```
> cd
> export PATH=~/miniconda3/bin:$PATH
> cd Assemblosis/Run
> cp ../Examples/assemblyCele.yml .

"Edit assemblyCele.yml to fit your computing environment and to define the location for the read files, databases and Illumina adapters"

> mkdir RepeatSimple; mkdir RepeatTransp; mkdir RepeatCustom
> cwltool --tmpdir-prefix /home/<username>/Tmp --beta-conda-dependencies --cachedir /home/<username>/Cache --user-space-docker-cmd udocker --leave-tmpdir assembly.cwl assemblyCele.yml
```

An annotated example of the YAML file for Caenorhabditis elegans assembly.
```
## Top level directory, which contains the PacBio raw data
# NOTE! The software looks for all .h5 files recursively in given directory
pacBioDataDir:
  class: Directory
  location: /home/<username>/Dna

## The directory where the assembly is run from
currentDir: /home/<username>/Assemblosis/Run

## Prefix for the resultant assembly files
prefix: cele

## Maximum number of threads used in the pipeline
threads: 24

### Parameters for the program Canu are described in https://canu.readthedocs.io/en/latest/parameter-reference.html
## Expected genome size. This parameter is forwarded to Canu assembler.
genomeSize: 100m

## Minimum length for the PacBio reads used for the assembly. This parameter is forwarded to Canu assembler.
# The maximum resolvable repeat regions becomes 2 x minReadLength
minReadLen: 6000

## Parameter for Canu assembler to adjust to GC-content. Should be 0.15 for high or low GC content.
corMaxEvidenceErate: 0.20

### Parameters for the program Trimmomatic are described in http://www.usadellab.org/cms/?page=trimmomatic
## Paired-end (PE) reads of Illumina raw data. These files are given to the program Trimmomatic.
# NOTE! Data for two paired libraries is given below.
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

### Parameters for the program bowtie2 are described in http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml
## Illumina PE fragment length. Program bowtie2 parameter -X.
# NOTE! Each read-pair needs one phred value.
maxFragmentLens: [500, 600]
# Orientation of pair-end reads e.g. 'fr', 'rf', 'ff': Program bowtie2 parameters --fr, --rf or --ff
orientation: 'fr'

### Parameters for the program Pilon are described in https://github.com/broadinstitute/pilon/wiki/Requirements-&-Usage
# Prefix for the resultant pilon polished assembly. Pilon parameter --output
polishedAssembly: celePilon
# This is set 'true' for an organism with diploid genome: Pilon parameter --diploid
diploidOrganism: true
# Value 'bases' fixes snps and indels: Pilon parameter --fix
fix: bases
# Generates a list or changes into a file if set 'true'. Pilon parameter --changes
modifications: true

### Parameters for the program centrifuge are described in http://www.ccb.jhu.edu/software/centrifuge/manual.shtml
# Path to the name of the index file, that contains NCBI nt database in nt.?.cf files. Centrifuge parameter -x
database: /home/<username>/nt
# Lenght of the identical match in nucleotides required to infer a read as contaminant. Centrifuge parameter --min-hitlen
partialMatch: 100
# NCBI taxon root identifers for the species considered contaminants: e.g. bacteria (=2), viruses (=10239), fungi (=4751), mammals (=40674), artificial seqs (=81077). Pipeline specific parameter.
taxons: [2,10239,4751,40674,81077]

## Parameters for the RepeatModeler and RepeatMasker are described in http://www.repeatmasker.org
repBaseLibrary:
  class: File
  # This is the RepBase file from https://www.girinst.org/repbase. RepeatMasker parameter -lib
  path: /home/<username>/RepBaseLibrary/RMRBSeqs.embl
# Directories for inferred custom repeats (inferred by RepeatModeler), tandem repeats (simple repeats) and interspersed repeats (transposons)'
# RepeatMasker parameter -dir
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

| Assembly | Runtime in CPU hours | RAM usage (GB) | Genome size (Mb) |
| --- | --- | --- | --- |
| *Caenorhabditis elegans* | 1537 | 134.1 | 100 |
| *Drosophila melanogaster* | 6501 | 134.1 | 138 |
| *Plasmodium falciparum* | 424 | 134.1 | 23 |
| *Haemonchus contortus* | 4704 | 142.1 | 320 |

Maximum memory usage of 134.1 GB and 142.1 GB was claimed by the program Centrifuge for each assembly. The difference in the usage is due to the updated NCBI nt database used for *Haemonchus contortus* assembly.

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

### Troubleshooting
Issue: Sometimes udocker fails to download the docker image. For instance:
```
Error: file size mismatch: /home/pakorhon/.udocker/layers/sha256:302e0c0de2a0989628fd78e574ccf4da76e2e14840bdf2199bb3bff951fbe739 2104908521 143291913
Error: no files downloaded
Error: image or container not available
```
Solution: Restart cwltool. Run should continue from the failed step when --leave-tmpdir option was used.

### Cite
If you use the pipeline, please cite: TBD

