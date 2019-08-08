cwlVersion: v1.0
class: CommandLineTool
id: "samtoolsIndex"
doc: "Indexes sorted the BAM file"
requirements:
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
      - $(inputs.inputBamFile)
inputs:
  - id: inputBamFile
    type: File
    inputBinding:
      position: 1

arguments:
  - valueFrom: $(inputs.inputBamFile.basename).bai
    position: 2

outputs:
  - id: sortedBamFile
    type: File
    outputBinding:
      glob: "$(inputs.inputBamFile.basename)"
  - id: bamIndexFile
    type: File
    outputBinding:
      glob: "$(inputs.inputBamFile.basename).bai"

baseCommand: [samtools, index]

hints:
  - class: DockerRequirement
    dockerPull: quay.io/biocontainers/samtools:1.6--0
