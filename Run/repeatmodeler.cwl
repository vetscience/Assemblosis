cwlVersion: v1.0
class: CommandLineTool
id: "RepeatMasker"
doc: "Infers genome specific repeats for given scaffolds"
requirements:
  - class: InlineJavascriptRequirement
#  - class: InitialWorkDirRequirement
#    listing:
#      - $(inputs.repBaseLibrary) 
hints:
  - class: DockerRequirement
    dockerPull: pakorhon/repeatmodeler:v1.0.12-beta
    #dockerPull: repeatmodeler:latest
inputs:
  - id: repBaseLibrary
    type: File
    #type: Directory
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
    #format: http://edamontology.org/format_1929  # FASTA
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
#  - id: workDir
#    type: Directory[]
#    #inputBinding:
#    #  position: 4
#    #  prefix: -recoverDir

outputs:
#  - id: repeatFastaFile
#    type:
#      type: array
#      items: [File, Directory]
#    outputBinding:
#      glob: "*"
  - id: repeatLibrary
    type: File
    outputBinding:
      glob: "*/RepeatMasker.lib"
  - id: repeatFastaFile
    type: File
    outputBinding:
      glob: "RM*/consensi.fa"
#  - id: outFile
#    type: File
#    outputBinding:
#      glob: "out"
  - id: repeatFastaFileClassified
    type: File?
    outputBinding:
      glob: "RM*/consensi.fa.classified"

baseCommand: ["RepeatModeler"]
arguments: []
#stdout: out
#stderr: err
#hints:
#  SoftwareRequirement:
#    packages:
#    - package: repeatmodeler
#      version:
#      - "1.0.8"
#      - "1.0.11"
