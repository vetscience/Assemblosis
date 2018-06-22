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
outputs:
  - id: trimmedReads
    type: File
    outputBinding:
      glob: "*/$(inputs.prefix).trimmedReads.fasta.gz"
baseCommand: ["canu","-trim"]
arguments: []
stdout: out
hints:
  SoftwareRequirement:
    packages:
    - package: canu
      version:
      - "1.6"
