cwlVersion: v1.0
class: CommandLineTool
id: "bowtie2-build"
doc: "Create a bowtie2 reference file"
requirements:
  - class: InlineJavascriptRequirement

inputs:
  - id: reference
    type: File
    inputBinding:
      position: 1

arguments:
  - valueFrom: $(inputs.reference.basename)
    position: 2

outputs:
  - id: indexFiles
    type: File[]
    outputBinding:
      glob: $(inputs.reference.basename).*

baseCommand: [bowtie2-build]

hints:
  - class: DockerRequirement
    dockerPull: quay.io/biocontainers/bowtie2:2.2.5--py36h2d50403_3
