cwlVersion: v1.0
class: CommandLineTool
id: "quiver"
doc: "Combine haplotypes in one sequence in a diploid genome"
requirements:
  - class: InlineJavascriptRequirement
hints:
  - class: DockerRequirement
    dockerPull: pakorhon/haplomerger:v0.0.7-beta
inputs:
  - id: assembly
    type: File
    inputBinding:
      position: 1
      prefix: -i
  - id: maskedAssembly
    type: File
    inputBinding:
      position: 2
      prefix: -m
  - id: trimmedReads
    type: File
    inputBinding:
      position: 3
      prefix: -r
  - id: threads
    type: int
    inputBinding:
      position: 4
      prefix: -T
outputs:
  - id: scoreMatrix
    type: File
    outputBinding:
      glob: "workDir/*/scoreMatrix.q"
  - id: mergedAssembly
    type: File
    outputBinding:
      glob: "workDir/*.haplomerged.fa*"
baseCommand: ["/home/haploMerger.sh"]
arguments: []
