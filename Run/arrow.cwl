cwlVersion: v1.0
class: CommandLineTool
id: "arrow"
doc: "Polish the assembly using PacBio reads"
requirements:
  - class: InlineJavascriptRequirement
hints:
  - class: DockerRequirement
    dockerPull: pakorhon/arrow:v0.0.4-beta
inputs:
  - id: dataDir
    type: Directory
    inputBinding:
      position: 1
      prefix: -d
  - id: assemblyDir
    type: string
    default: CanuAssembly
    inputBinding:
      position: 2
      prefix: -a
  - id: assembly
    type: File
    inputBinding:
      position: 3
      prefix: -s
  - id: prefix
    type: string
    inputBinding:
      position: 4
      prefix: -p
outputs:
  - id: assembled
    type:
      type: array
      items: [File, Directory]
    outputBinding:
      glob: "*"
  - id: arrowPolishedAssembly
    type: File
    format: edam:format_1929  # fasta
    outputBinding:
      glob: "$(inputs.prefix).contigs.arrowed.fasta"
baseCommand: ["/root/Assemblosis/smrtpipe.sh"]
arguments: []
