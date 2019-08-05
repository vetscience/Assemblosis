cwlVersion: v1.0
class: CommandLineTool
id: "centrifuge"
doc: "Decontaminate PacBio reads using the program centrifuge"
requirements:
  - class: InlineJavascriptRequirement
hints:
  - class: DockerRequirement
    dockerPull: pakorhon/decon:v0.0.5-beta
inputs:
  - id: prefix
    type: string
    inputBinding:
      position: 1
      prefix: -r
  - id: trimmedReads
    type: File
    inputBinding:
      position: 1
      prefix: -U
  - id : classificationFile
    type: File
    default: classification.txt
    inputBinding:
      position: 2
      prefix: -S
  - id : taxons
    type:
      type: array
      items: int
    inputBinding:
      position: 3
      itemSeparator: ","
      separate: true
      prefix: -t
  - id : mappedIds
    type: File
    inputBinding:
      position: 4
      prefix: -m
  - id : partialMatch
    type: int
    default: 100
    inputBinding:
      position: 5
      prefix: -p
outputs:
  - id: conReads
    type: File
    outputBinding:
      glob: "$(inputs.prefix).contaminatedReads.fasta.gz"
  - id: deconReads
    type: File
    outputBinding:
      glob: "$(inputs.prefix).trimmedReads.fasta.gz"
  - id: deconReadIds
    type: File
    outputBinding:
      glob: "contaminated.read.ids.unique"
  - id: contaminatedReadsIds
    type: File
    outputBinding:
      glob: "taxon.ids"
  - id: classificationConverted
    type: File
    outputBinding:
      glob: "classification.converted"
baseCommand: ["bash","/home/decon.sh"]
arguments: []
