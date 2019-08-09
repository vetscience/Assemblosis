cwlVersion: v1.0
class: CommandLineTool
id: "RepeatMasker"
doc: "Masks given genomic scaffolds using given mask option and/or repeat file"
requirements:
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
      - $(inputs.repeatLibrary)

inputs:
  - id: threads
    type: int
    inputBinding:
      prefix: -pa
      position: 2
  - id: engine
    type: string
    default: ncbi
    inputBinding:
      prefix: -engine
      position: 3
  - id: density
    type: boolean
    default: true
    inputBinding:
      position: 3
      prefix: -excln
  - id: calculateGc
    type: boolean
    default: true
    inputBinding:
      position: 4
      prefix: -gccalc
  - id: slowSearch
    type: boolean
    default: true
    inputBinding:
      position: 5
      prefix: -s
  - id: skipBacterial
    type: boolean
    default: true
    inputBinding:
      position: 6
      prefix: -no_is
  - id: createGff
    type: boolean
    default: true
    inputBinding:
      position: 7
      prefix: -gff
  - id: noInterspersed
    type: boolean
    inputBinding:
      position: 8
      prefix: -noint
  - id: noLowComplexity
    type: boolean
    inputBinding:
      position: 9
      prefix: -nolow
  - id: repeatLibrary
    type: File
    inputBinding:
      position: 10
      prefix: -lib
  - id: reference
    type: File
    inputBinding:
      position: 11

outputs:
  - id: categoryFile
    type: File
    outputBinding:
      glob: "$(inputs.reference.basename).cat*"

baseCommand: ["RepeatMasker"]
arguments: ["-dir", $(runtime.outdir)]
hints:
  - class: DockerRequirement
    dockerPull: quay.io/biocontainers/repeatmasker:4.0.6--pl5.22.0_10
