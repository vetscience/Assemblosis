cwlVersion: v1.0
class: CommandLineTool
id: "bowtie2-build"
doc: "Create a bowtie2 reference file"
requirements:
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
      - $(inputs.reference)

inputs:
  - id: reference
    type: File
    inputBinding:
      position: 1

arguments:
  - valueFrom: $(inputs.reference.basename)
    position: 2

outputs:
#  - id: indexFiles
#    type: File
#    outputBinding:
#      glob: $(inputs.reference.basename).*
  - id: referenceAssembly
    type: File
    outputBinding:
      glob: "$(inputs.reference.basename)"
  - id: bt2_1
    type: File
    outputBinding:
      glob: "$(inputs.reference.basename).1.bt2"
  - id: bt2_2
    type: File
    outputBinding:
      glob: "$(inputs.reference.basename).2.bt2"
  - id: bt2_3
    type: File
    outputBinding:
      glob: "$(inputs.reference.basename).3.bt2"
  - id: bt2_4
    type: File
    outputBinding:
      glob: "$(inputs.reference.basename).4.bt2"
  - id: bt2rev1
    type: File
    outputBinding:
      glob: "$(inputs.reference.basename).rev.1.bt2"
  - id: bt2rev2
    type: File
    outputBinding:
      glob: "$(inputs.reference.basename).rev.2.bt2"

baseCommand: [bowtie2-build]

hints:
  - class: DockerRequirement
    dockerPull: quay.io/biocontainers/bowtie2:2.2.5--py36h2d50403_3
