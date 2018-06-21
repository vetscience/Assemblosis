cwlVersion: v1.0
class: CommandLineTool
id: "samtoolsIndex"
doc: "Indexes sorted the BAM file"
requirements:
  - class: InlineJavascriptRequirement
#  - class: InitialWorkDirRequirement
#    listing:
#      - $(inputs.inputBamFile.path)
#hints:
#  - class: DockerRequirement
#    dockerPull: samindex:latest
inputs:
  - id: inputBamFile
    type: File
    #format: edam:format_2572  # BAM format
    inputBinding:
      position: 1

arguments:
  - valueFrom: $(inputs.inputBamFile.basename).bai
    position: 2

#arguments:
#  - valueFrom: mapped.$(inputs.inputBamFile.basename).bai
#    position: 2

outputs:
  - id: bamIndexFile
    type: File[]
    #format: edam:format_3327  # BAI format
    outputBinding:
      glob: "$(inputs.inputBamFile.basename).bai"
#  - id: indexedBamFile
#    type: File
#    format: edam:format_2572  # BAM format
#    outputBinding:
#      glob: mapped.$(inputs.inputBamFile.basename)
#    secondaryFiles:
#      - .bai

baseCommand: [samtools, index]

#stdout: mapped.$(inputs.inputBamFile.basename)

hints:
  SoftwareRequirement:
    packages:
    - package: samtools
      version:
      - "1.6"
