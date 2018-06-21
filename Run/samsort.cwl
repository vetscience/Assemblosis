cwlVersion: v1.0
class: CommandLineTool
id: "samtoolsSort"
doc: "Sorts the SAM file to a BAM file"
requirements:
  - class: InlineJavascriptRequirement
inputs:
  - id: threads
    type: int
    default: 1
    inputBinding:
      position: 1
      prefix: -@
  - id: inputSamFile
    type: File
    inputBinding:
      position: 3

arguments:
  - valueFrom: $(inputs.inputSamFile.basename.slice(0,-4)).bam
    prefix: -o
    position: 2
  #- id: outputBamFile
  #  type: string
  #  inputBinding:
  #    prefix: -o
  #    position: 2

outputs:
  - id: sortedBamFile
    type: File
    #format: edam:format_2572  # BAM format
    outputBinding:
      glob: "*.bam"

baseCommand: [samtools, sort]

#stdout: bowtie2.sorted.bam
hints:
  SoftwareRequirement:
    packages:
    - package: samtools
      version:
      - "1.6"
