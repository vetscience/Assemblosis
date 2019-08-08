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
  - id: minReadLen
    type: int
    default: 6000
    inputBinding:
      position: 5
      separate: false
      prefix: minReadLength=
  - id: pacbio-corrected
    type: File
    inputBinding:
      position: 6
      prefix: -pacbio-corrected
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
  - id: obtmhapConcurrency
    type: int
    default: 6
    inputBinding:
      position: 16
      separate: false
      prefix: obtmhapConcurrency=
  - id: utgmhapConcurrency
    type: int
    default: 6
    inputBinding:
      position: 17
      separate: false
      prefix: utgmhapConcurrency=
  - id: obtmmapConcurrency
    type: int
    default: 6
    inputBinding:
      position: 16
      separate: false
      prefix: obtmmapConcurrency=
  - id: utgmmapConcurrency
    type: int
    default: 6
    inputBinding:
      position: 17
      separate: false
      prefix: utgmmapConcurrency=
  - id: obtovlConcurrency
    type: int
    default: 6
    inputBinding:
      position: 16
      separate: false
      prefix: obtovlConcurrency=
  - id: utgovlConcurrency
    type: int
    default: 6
    inputBinding:
      position: 17
      separate: false
      prefix: utgovlConcurrency=
outputs:
  - id: trimmedReads
    type: File
    outputBinding:
      glob: "*/$(inputs.prefix).trimmedReads.fasta.gz"
  - id: assembly
    type: File
    outputBinding:
      glob: "*/$(inputs.prefix).contigs.fasta"
baseCommand: ["canu", "-trim-assemble"]
arguments: []
stdout: out
hints:
  - class: DockerRequirement
    dockerPull: quay.io/biocontainers/canu:1.8--pl526h470a237_0
