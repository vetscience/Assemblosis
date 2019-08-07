cwlVersion: v1.0
class: CommandLineTool
id: "trimmomaticpe"
doc: "Clean paired-end Illumina reads"
requirements:
  - "$import": assembly-typedef.yml
  - class: InlineJavascriptRequirement
  - class: EnvVarRequirement
    envDef:
      CLASSPATH: /usr/local/share/trimmomatic-0.36-5/trimmomatic.jar

inputs:
  - id: phred
    type: string
    default: '33'
    inputBinding:
      prefix: -phred
      separate: false
      position: 1
  - id: threads
    type: int
    default: 1
    inputBinding:
      position: 2
      prefix: -threads
  - id: reads1
    type: File
    format: edam:format_1930  # fastq
    inputBinding:
      position: 3
  - id: reads2
    type: File
    format: edam:format_1930  # fastq
    inputBinding:
      position: 4
  - id: slidingWindow
    type: assembly-typedef.yml#slidingWindow?
    inputBinding:
      position: 9
      valueFrom: SLIDINGWINDOW:$(self.windowSize):$(self.requiredQuality)
  - id: illuminaClip
    type: assembly-typedef.yml#illuminaClipping?
    inputBinding:
      valueFrom: ILLUMINACLIP:$(self.adapters.path):$(self.seedMismatches):$(self.palindromeClipThreshold):$(self.simpleClipThreshold):$(self.minAdapterLength):$(self.keepBothReads)
#      valueFrom: |
#        ILLUMINACLIP:$(self.adapters.path):$(self.seedMismatches):$(self.palindromeClipThreshold):$(self.simpleClipThreshold):$(self.minAdapterLength):$(self.keepBothReads)
      position: 10
  - id: leading
    type: int?
    inputBinding:
      position: 11
      prefix: 'LEADING:'
      separate: false
  - id: trailing
    type: int?
    inputBinding:
      position: 12
      prefix: 'TRAILING:'
      separate: false
  - id: minlen
    type: int?
    inputBinding:
      position: 13
      prefix: 'MINLEN:'
      separate: false
  - id: headcrop
    type: int?
    inputBinding:
      position: 14
      prefix: 'HEADCROP:'
      separate: false
  - id: avgqual
    type: int?
    inputBinding:
      position: 15
      prefix: 'AVGQUAL:'
      separate: false

arguments:
- valueFrom: pe1.$(inputs.reads1.nameroot).fastq.gz
  position: 5
- valueFrom: unpe1.$(inputs.reads1.nameroot).fastq.gz
  position: 6
- valueFrom: pe2.$(inputs.reads2.nameroot).fastq.gz
  position: 7
- valueFrom: unpe2.$(inputs.reads2.nameroot).fastq.gz
  position: 8
- valueFrom: trim.log
  prefix: -trimlog 
  position: 16

outputs:
  - id: trimmedPe1
    type: File
    format: edam:format_1930  # fastq
    outputBinding:
      glob: pe1.$(inputs.reads1.nameroot).fastq.gz
  - id: trimmedUnpe1
    type: File
    format: edam:format_1930  # fastq
    outputBinding:
      glob: unpe1.$(inputs.reads1.nameroot).fastq.gz
  - id: trimmedPe2
    type: File
    format: edam:format_1930  # fastq
    outputBinding:
      glob: pe2.$(inputs.reads2.nameroot).fastq.gz
  - id: trimmedUnpe2
    type: File
    format: edam:format_1930  # fastq
    outputBinding:
      glob: unpe2.$(inputs.reads2.nameroot).fastq.gz
  - id: trimLogFile
    type: File
    outputBinding:
      glob: trim.log
    label: Trimmomatic log

baseCommand: [java,org.usadellab.trimmomatic.TrimmomaticPE]
hints:
  - class: DockerRequirement
    dockerPull: "quay.io/biocontainers/trimmomatic:0.36--5"
