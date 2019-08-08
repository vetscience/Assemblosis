cwlVersion: v1.0
class: CommandLineTool
id: "BuildDatabase"
doc: "Build an indexed database for RepeatModeler from given scaffolds"
requirements:
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
      - $(inputs.scaffolds)
 
inputs:
  - id: engine
    type: string
    default: ncbi
    inputBinding:
      prefix: -engine
      position: 2
  - id: scaffolds
    type: File
    inputBinding:
      position: 3

outputs:
#  - id: indexFiles
#    type: File[]
#    outputBinding:
#      glob: "$(inputs.scaffolds.basename).*"
  - id: pilonPolishedAssembly
    type: File
    outputBinding:
      glob: "$(inputs.scaffolds.basename)"
  - id: translation
    type: File
    outputBinding:
      glob: "$(inputs.scaffolds.basename).translation"
  - id: nsq
    type: File
    outputBinding:
      glob: "$(inputs.scaffolds.basename).nsq"
  - id: nin
    type: File
    outputBinding:
      glob: "$(inputs.scaffolds.basename).nin"
  - id: nhr
    type: File
    outputBinding:
      glob: "$(inputs.scaffolds.basename).nhr"
  - id: nog
    type: File
    outputBinding:
      glob: "$(inputs.scaffolds.basename).nog"
  - id: nni
    type: File
    outputBinding:
      glob: "$(inputs.scaffolds.basename).nni"
  - id: nnd
    type: File
    outputBinding:
      glob: "$(inputs.scaffolds.basename).nnd"

baseCommand: ["BuildDatabase"]
arguments:
- -name
- valueFrom: $(inputs.scaffolds.basename)
hints:
  - class: DockerRequirement
    dockerPull: quay.io/biocontainers/repeatmodeler:1.0.11--pl526_1
