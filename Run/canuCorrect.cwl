cwlVersion: v1.0
class: CommandLineTool
id: "canu"
doc: "Assemble PacBio reads (canu -correct -trim -assemble)"
requirements:
  - class: InlineJavascriptRequirement
inputs:
  - id: prefix
    type: string
    inputBinding:
      position: 1
      prefix: -p
  - id: assemblyDir
    type: string
    default: CanuAssembly
    inputBinding:
      position: 2
      prefix: -d
  - id: genomeSize
    type: string
    inputBinding:
      position: 3
      separate: false
      prefix: genomeSize=
  - id: stopOnReadQuality
    type: string
    default: "true"
    inputBinding:
      position: 4
      separate: false
      prefix: stopOnReadQuality=
  - id: pacbio-raw
    type: File
    inputBinding:
      position: 6
      prefix: -pacbio-raw
  - id: corMaxEvidenceErate
    type: float
    default: 0.20
    inputBinding:
      position: 7
      separate: false
      prefix: corMaxEvidenceErate=
  - id: useGrid
    type: string
    default: "false"
    inputBinding:
      position: 10
      separate: false
      prefix: useGrid=
#  - id: ovsMethod
#    type: string
#    default: "sequential"
#    inputBinding:
#      position: 11
#      separate: false
#      prefix: ovsMethod=
#  - id: gnuplotTested
#    type: string
#    default: "true"
#    inputBinding:
#      position: 12
#      separate: false
#      prefix: gnuplotTested=
  - id: minThreads
    type: int
    inputBinding:
      position: 13
      separate: false
      prefix: minThreads=
  - id: maxThreads
    type: int
    inputBinding:
      position: 14
      separate: false
      prefix: maxThreads=
  - id: corConcurrency
    type: int
    default: 6
    inputBinding:
      position: 15
      separate: false
      prefix: corConcurrency=
outputs:
  - id: correctedReads
    type: File
    outputBinding:
      glob: "*/$(inputs.prefix).correctedReads.fasta.gz"
baseCommand: ["canu", "-correct"]
arguments: []
stdout: out
hints:
  - class: DockerRequirement
    dockerPull: quay.io/biocontainers/canu:1.8--pl526h470a237_0
