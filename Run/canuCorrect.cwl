cwlVersion: v1.0
class: CommandLineTool
id: "canu"
doc: "Assemble PacBio reads (canu -correct -trim -assemble)"
requirements:
  - class: InlineJavascriptRequirement
#  - class: InitialWorkDirRequirement
#    listing: $(runtime.outdir)/$(inputs.workDir.listing)
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
#  - id: errorRate
#    type: float
#    default: 0.025
#    inputBinding:
#      position: 5
#      separate: false
#      prefix: errorRate=
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
 # - id: corOutCoverage
 #   type: float
 #   default: 200
 #   inputBinding:
 #     position: 8
 #     separate: false
 #     prefix: corOutCoverage=
 # - id: ovlErrorRate
 #   type: float
 #   default: 0.15
 #   inputBinding:
 #     position: 9
 #     separate: false
 #     prefix: ovlErrorRate=
 # - id: obtErrorRate
 #   type: float
 #   default: 0.15
 #   inputBinding:
 #     position: 9
 #     separate: false
 #     prefix: obtErrorRate=
  - id: useGrid
    type: string
    default: "false"
    inputBinding:
      position: 10
      separate: false
      prefix: useGrid=
#  - id: gripOptions
#    type: string
#    default: ""
#    inputBinding:
#      position: 7
#      prefix: gridOptions=
outputs:
#  - id: assembled
#    type:
#      type: array
#      items: [File, Directory]
#    outputBinding:
#      glob: "*"
#  - id: assembled
#    type:
#      type: array
#      items: [File, Directory]
#    outputBinding:
#      glob: "$inputs.workDir"
#  - id: assembly
#    type:
#      type: array
#      items: File
#    outputBinding:
#      #glob: "$(inputs.workDir)/$(inputs.prefix).contigs.fasta"
#      glob: "*/$inputs.prefix.contigs.fasta"
  - id: correctedReads
    type: File
    outputBinding:
      glob: "*/$(inputs.prefix).correctedReads.fasta.gz"
baseCommand: ["canu", "-correct"]
arguments: []
stdout: out
hints:
  SoftwareRequirement:
    packages:
    - package: canu
      version:
      - "1.6"
