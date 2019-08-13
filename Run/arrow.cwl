cwlVersion: v1.0
class: CommandLineTool
id: "arrow"
doc: "Polish the assembly using PacBio reads"
requirements:
  - class: InlineJavascriptRequirement
hints:
  - class: DockerRequirement
    dockerPull: pakorhon/arrow:v0.0.7-beta
inputs:
  - id: dataDir
    type: Directory
    inputBinding:
      position: 1
      prefix: -d
  - id: tmpDir
    type: string
    inputBinding:
      position: 2
      prefix: -t
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
  - id: bam
    type: boolean
    default: false
    inputBinding:
      prefix: -b
      position: 5
outputs:
  - id: arrowPolishedAssembly
    type: File
    format: edam:format_1929  # fasta
    outputBinding:
      glob: "$(inputs.prefix).contigs.arrowed.fasta"
baseCommand: ["/home/Assemblosis/smrtpipe.sh"]
arguments: []
