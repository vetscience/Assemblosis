cwlVersion: v1.0
class: CommandLineTool
id: "RepeatMasker"
doc: "Infers genome specific repeats for given scaffolds"
requirements:
  - class: InlineJavascriptRequirement
hints:
  - class: DockerRequirement
    dockerPull: pakorhon/repeatmodeler:v0.0.6-beta
inputs:
  - id: repBaseLibrary
    type: File
  - id: engine
    type: string
    default: ncbi
    inputBinding:
      prefix: -engine
      position: 1
  - id: threads
    type: int
    inputBinding:
      prefix: -pa
      position: 2
  - id: database
    type: File
    inputBinding:
      position: 3
      prefix: -database
    secondaryFiles:
      - .translation
      - .nsq
      - .nin
      - .nhr
      - .nog
      - .nni
      - .nnd

outputs:
  - id: repeatLibrary
    type: File
    outputBinding:
      glob: "*/RepeatMasker.lib"
  - id: repeatFastaFile
    type: File
    outputBinding:
      glob: "RM*/consensi.fa"
#  - id: repeatFastaFileClassified
#    type: File?
#    outputBinding:
#      glob: "RM*/consensi.fa.classified"

baseCommand: ["/home/repeatModeler.sh"]
arguments: []
