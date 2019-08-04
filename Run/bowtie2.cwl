cwlVersion: v1.0
class: CommandLineTool
id: "bowtie2"
doc: "Maps illumina reads to a genome"
requirements:
  - class: InlineJavascriptRequirement
inputs:
  - id: seedMismatches
    type: string
    default: '1'
    inputBinding:
      prefix: -N
      position: 1
  - id: phred
    type: string
    default: '33'
    inputBinding:
      prefix: --phred
      separate: false
      position: 2
  - id: orientation
    type: string
    default: 'fr'
    inputBinding:
      prefix: --
      separate: false
      position: 3
  - id: threads
    type: int
    default: 1
    inputBinding:
      position: 4
      prefix: --threads
  - id: maxFragmentLen
    type: int
    default: 500
    inputBinding:
      position: 5
      prefix: -X
  - id: reference
    type: File
    inputBinding:
      position: 6
      prefix: -x
    secondaryFiles:
      - .1.bt2
      - .2.bt2
      - .3.bt2
      - .4.bt2
      - .rev.1.bt2
      - .rev.2.bt2
  - id: reads1
    type: File
    inputBinding:
      prefix: "-1"
      position: 7
  - id: reads2
    type: File
    inputBinding:
      prefix: "-2"
      position: 8

outputs:
  - id: samFile
    type: File
    format: edam:format_2573  # SAM format
    outputBinding:
      glob: $(inputs.reads1.basename.slice(0,-9)).sam

baseCommand: [bowtie2]

stdout: $(inputs.reads1.basename.slice(0,-9)).sam
hints:
  - class: DockerRequirement
    dockerPull: quay.io/biocontainers/bowtie2:2.2.5--py36h2d50403_3
