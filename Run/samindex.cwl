cwlVersion: v1.0
class: CommandLineTool
id: "samtoolsIndex"
doc: "Indexes sorted the BAM file"
requirements:
  - class: InlineJavascriptRequirement
inputs:
  - id: inputBamFile
    type: File
    inputBinding:
      position: 1

arguments:
  - valueFrom: $(inputs.inputBamFile.basename).bai
    position: 2

outputs:
  - id: bamIndexFile
    type: File[]
    outputBinding:
      glob: "$(inputs.inputBamFile.basename).bai"

baseCommand: [samtools, index]

hints:
  SoftwareRequirement:
    packages:
    - package: samtools
      version:
      - "1.6"
