cwlVersion: cwl:v1.0
class: CommandLineTool
requirements:
  - class: InlineJavascriptRequirement
hints:
  - class: DockerRequirement
    dockerPull: pakorhon/combinecats:v0.0.4-beta
inputs:
  - id: assembly
    type: File
    inputBinding:
      prefix: -a
      position: 2
  - id: categories
    type: File[]
    inputBinding:
      prefix: -c
      position: 3
      separate: true
      itemSeparator: ","
outputs:
  - id: repResFiles
    type: File[]
    outputBinding:
      glob: "*/all.*"
  - id: maskedAssembly
    type: File
    outputBinding:
      glob: "*/$(inputs.assembly.basename).masked"
baseCommand: ["bash","/home/combine.sh"]
