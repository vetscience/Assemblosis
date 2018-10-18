cwlVersion: v1.0
class: CommandLineTool
id: "centrifuge"
doc: "Classify PacBio reads using the program centrifuge"
requirements:
  - class: InlineJavascriptRequirement
inputs:
  - id: database
    type: Directory
#    inputBinding:
#      position: 1
#      prefix: -x
  - id: trimmedReads
    type: File
    inputBinding:
      position: 3
      prefix: -U
  - id: threads
    type: int
    inputBinding:
      position: 4
      prefix: -p
  - id: reportFile
    type: string
    default: report.txt
    inputBinding:
      position: 5
      prefix: --report-file
  - id: classificationFile
    type: string
    default: classification.txt
    inputBinding:
      position: 6
      prefix: -S
  - id: partialMatch
    type: int
    default: 100
    inputBinding:
      position: 7
      prefix: --min-hitlen
outputs:
  - id: report
    type: File
    outputBinding:
      glob: "$(inputs.reportFile)"
  - id: classification
    type: File
    outputBinding:
      glob: "$(inputs.classificationFile)"
baseCommand: ["centrifuge","-f"]
arguments:
- valueFrom: $(inputs.database.path)/nt
  prefix: -x
  position: 1
hints:
  - class: DockerRequirement
    dockerPull: quay.io/biocontainers/centrifuge:1.0.3--py27pl5.22.0_3
