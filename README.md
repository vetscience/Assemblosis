## CWL based workflow to assemble haploid/diploid eukaryote genomes of non-model organisms
The workflow is designed to use both PacBio long-reads and Illumina short-reads. The workflow first extracts, corrects, trims and decontaminates the long reads. Decontaminated trimmed reads are then used to assemble the genome and raw reads are used to polish it. Next, Illumina reads are cleaned and used to further polish the resultant assembly. Finally, the polished assembly is masked using inferred repeats and haplotypes are eliminated. The workflow uses BioConda and DockerHub to install required software and is therefore fully automated. In addition to final assembly, the workflow produces intermediate assemblies before and after polishing steps. The workflow follows the syntax for CWL v1.0 and has been tested using the reference implementations in Dell server of 24 CPUs.

### Dependencies
Programs
* [udocker v1.1.1](https://github.com/indigo-dc/udocker)
* [cwltool v1.0.20180403145700](https://github.com/common-workflow-language/cwltool)
* [Python library galaxy-lib v18.5.7](https://pypi.org/project/galaxy-lib)

Data
* [Illumina adapters converted to FASTA format](http://sapac.support.illumina.com/downloads/illumina-adapter-sequences-document-1000000002694.html)
* [NCBI nucleotide non-redundant sequences for decontamination with Centrifuge](http://www.ccb.jhu.edu/software/centrifuge)
* [RepBase v17.02](https://www.girinst.org/repbase)

### Installation
Follow installation guidelines given for each program (udocker, cwltool and galaxy-lib) in their web-sites.
After installing cwltool, apply following fix in the file site-packages/cwltool/job.py
```
471,473c471,472
<         if env != None: # This is the fix
<             for key in env:
<                 env_copy[key] = env[key]
---
>         for key in env:
>             env_copy[key] = env[key]
```
Download and extract RepBase database, Centrifuge version of NCBI nt database and create Illumina adapter FASTA file to your preferred location.

### Usage
You have to create a YAML (.yml) file for each assembly. This file defines the required parameters and the location for both PacBio and Illumina raw-reads.
```
> cd Run
> cp ../Examples/assemblyCele.yml

"Edit assemblyCele.yml to fit your computing environment and to define the location for the read files, databases and Illumina adapters"

> mkdir RepeatSimple; mkdir RepeatTransp; mkdir RepeatCustom
> cwltool --tmpdir-prefix /home/<username>/Tmp --beta-conda-dependencies --cachedir /home/<username>/Cache --user-space-docker-cmd udocker --leave-tmpdir assembly.cwl assemblyCele.yml
```
An annotated example of the YAML file for Caenorhabditis elegans assembly.
```
# Root of the directory, which contains the PacBio raw data
pacBioDataDir:
  class: Directory
  location: /home/<username>/Dna
currentDir: /home/<username>/Assembler/Run # The directory where the assembly is run from
prefix: cele # Prefix for the resultant assembly files
genomeSize: 100m # Expected genome size
minReadLen: 6000 # Minimum length for the reads used for the assembly
corMaxEvidenceErate: 0.20  # Parameter for Canu assembler to adjust to GC-content. Should be 0.15 for high or log GC content.
# Paired-end (PE) reads for Illumina data
readsPe1:
  - class: File
    format: edam:format_1930  # fastq
    path: /home/<username>/Dna/SRR2598966_1.fastq.gz
readsPe2:
  - class: File
    format: edam:format_1930  # fastq
    path: /home/<username>/Dna/SRR2598966_2.r.fastq.gz # Reversed reads
phredsPe: ['33'] # Phred coding of Illumina data
# Sliding window and illuminaClip parameters for Trimmomatic
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
# Further parameters for Trimmomatic
leading: 25
trailing: 25
minlen: 40

threads: 24 # Maximum number of threads used in the pipeline

maxFragmentLens: [500] # Illumina PE fragment length

# Parameters for the program Pilon
orientation: 'fr'
polishedAssembly: celePilon # Prefix for the resultant assembly
diploidOrganism: true
fix: bases
modifications: true

# Parameters for the program Centrifuge to remove listed contaminations
database: /home/<username>/nt
taxons: [2,10239,4751,40674,81077] # Bacteria, viruses, fungi, mammals, artificial seqs
partialMatch: 100

# Parameters for the RepeatModeler and RepeatMasker
repBaseLibrary:
  class: File
  path: /home/<username>/RepBaseLibrary/RMRBSeqs.embl # This is the RepBase file from https://www.girinst.org/repbase
repeatWorkDir:
  - class: Directory
    location: RepeatCustom
  - class: Directory
    location: RepeatSimple
  - class: Directory
    location: RepeatTransp
noInterspersed: [false, true, false]
noLowComplexity: [true, false, true]
```

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

