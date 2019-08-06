cwlVersion: v1.0
class: CommandLineTool
id: "table"
doc: "Create a table for metrics"
requirements:
  - class: InlineJavascriptRequirement
hints:
  - class: DockerRequirement
    dockerPull: pakorhon/collect:v0.0.4-beta
inputs:
  - id: reference
    type: File
    inputBinding:
      position: 1
      prefix: -r
  - id: assemblies
    type: File[]
    inputBinding:
      position: 2
      prefix: -a
      itemSeparator: ","
  - id: gageResults
    type: File[]
    inputBinding:
      position: 3
      prefix: -g
      itemSeparator: ","
  - id: quastResults
    type: File[]
    inputBinding:
      prefix: -q
      position: 4
      itemSeparator: ","
  - id: quastMisassemblies
    type: File[]
    inputBinding:
      prefix: -m
      position: 5
      itemSeparator: ","
  - id: quastSnpsZipped
    type: File[]
    inputBinding:
      prefix: -s
      position: 6
      itemSeparator: ","
  - id: refGff
    type: File
    inputBinding:
      position: 7
      prefix: -f
  - id: buscoResults
    type: File[]
    inputBinding:
      prefix: -b
      position: 8
      itemSeparator: ","
  - id: labels
    type: string[]
    inputBinding:
      position: 9
      prefix: -l
      itemSeparator: ","
outputs:
  - id: table
    type: File
    outputBinding:
      glob: "metrics.txt"
baseCommand: ["python", "/root/createTables.py"]
stdout: metrics.txt
