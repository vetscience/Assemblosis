cwlVersion: v1.0
class: CommandLineTool
id: "RepeatMasker"
doc: "Masks given genomic scaffolds using given mask option and/or repeat file"
requirements:
#  - $import: pilon-typedef.yml
  - class: InlineJavascriptRequirement
#  - class: EnvVarRequirement
#    envDef:
#      #CLASSPATH: $(inputs.currentDir)/cwltool_deps/_conda/envs/__pilon@1.20/share/pilon-1.20-1/pilon-1.20.jar
#      CLASSPATH: $(inputs.currentDir)/cwltool_deps/_conda/envs/__pilon@1.22/share/pilon-1.22-0/pilon-1.22.jar
#  - class: InitialWorkDirRequirement
#    listing: $(runtime.outdir)/$(inputs.workDir.listing)
  - class: InitialWorkDirRequirement
    #listing: [ $(inputs.bamPeIdx), $(inputs.bamPe) ]
    listing:
      - $(inputs.workDir)
#      - $(inputs.repBaseLibrary) 
#hints:
#  - class: DockerRequirement
#    dockerPull: repeatmasker:latest

inputs:
#  - id: repBaseLibrary
#    type: Directory
  - id: workDir
    type: Directory
    #type: string
    inputBinding:
      prefix: -dir
      position: 1
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
    type: File?
    inputBinding:
      position: 10
      prefix: -lib
  - id: reference
    type: File
    #format: edam:format_1929  # FASTA
    inputBinding:
      position: 11

outputs:
#  - id: repeatFastaFile
#    type:
#      type: array
#      items: [File, Directory]
#    outputBinding:
#      glob: "*"
#  - id: outFile
#    type: File
#    outputBinding:
#      glob: "out"
  - id: categoryFile
    type: File
    outputBinding:
      glob: "*/$(inputs.reference.basename).cat*"

baseCommand: ["RepeatMasker"]
arguments: []
#stdout: out
hints:
  SoftwareRequirement:
    packages:
    - package: repeatmasker
      version:
      - "4.0.6"
