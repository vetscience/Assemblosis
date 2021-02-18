cwlVersion: v1.0
class: CommandLineTool
id: "removeBubbles"
doc: "Remove bubble contigs from assembled genome"
requirements:
  - class: InlineJavascriptRequirement
hints:
  - class: DockerRequirement
    dockerPull: pakorhon/removebubbles:v0.0.1-beta
inputs:
  - id: contigs
    type: File
    inputBinding:
      prefix: -a
      position: 1
outputs:
  - id: assembly
    type: File
    outputBinding:
      glob: "filtered.$(inputs.contigs.basename)"
baseCommand: ["bash","/home/rmBubbles.sh"]
