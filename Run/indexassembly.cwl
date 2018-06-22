cwlVersion: v1.0
class: CommandLineTool
id: "BuildDatabase"
doc: "Build an indexed database for RepeatModeler from given scaffolds"
requirements:
  - class: InlineJavascriptRequirement
 
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
  - id: indexFiles
    type: File[]
    outputBinding:
      glob: "$(inputs.scaffolds.basename).*"

baseCommand: ["BuildDatabase"]
arguments:
- -name
- valueFrom: $(inputs.scaffolds.basename)
hints:
  SoftwareRequirement:
    packages:
    - package: repeatmodeler
      version:
      - "1.0.11"
