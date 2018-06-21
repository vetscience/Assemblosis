cwlVersion: v1.0
class: CommandLineTool
id: "pilon"
doc: "Polishing an assembly using Illumina reads"
requirements:
#  - $import: pilon-typedef.yml
  - class: InlineJavascriptRequirement
  - class: EnvVarRequirement
    envDef:
      #CLASSPATH: $(inputs.currentDir)/cwltool_deps/_conda/envs/__pilon@1.20/share/pilon-1.20-1/pilon-1.20.jar
      CLASSPATH: $(inputs.currentDir)/cwltool_deps/_conda/envs/__pilon@1.22/share/pilon-1.22-0/pilon-1.22.jar
#  - class: InitialWorkDirRequirement
#    listing: [ $(inputs.bamPeIdx), $(inputs.bamPe) ]
 
inputs:
#  - id: java_opts
#    type: string
#    #default: "-Xms8g Xmx32g"
#    inputBinding:
#      position: 0
#      shellQuote: false
  - id: currentDir
    type: string
#  - id: bamPeIdx
#    type: File
  - id: reference
    type: File
    #format: edam:format_1929  # FASTA
    inputBinding:
      prefix: --genome
      position: 1
  - id: bamPe
    type: File[]
#    #format: edam:format_2572  # BAM format
#    inputBinding:
#      prefix: --frags
#      itemSeparator: "\t--frags\t"
#      position: 2
#      #shellQuote: false
    secondaryFiles:
      - .bai
  - id: output
    type: string
    inputBinding:
      prefix: --output
      position: 3
  - id: diploidOrganism
    type: boolean
    #type: pilon-typedef.yml#diploid
    inputBinding:
      prefix: --diploid
      position: 4
  - id: fix
    type: string
    inputBinding:
      prefix: --fix
      position: 5
  - id: modifications
    type: boolean
    #type: pilon-typedef.yml#changes
    inputBinding:
      prefix: --changes
      position: 6
  - id: threads
    type: int
    default: 1
    inputBinding:
      position: 7
      prefix: --threads

arguments:
- valueFrom: ${var r = []; for (var i = 0; i < inputs.bamPe.length; i++) { r.push("--frags"); r.push(inputs.bamPe[i].path); } return r; }
  #prefix: --frags
  position: 2

outputs:
  - id: pilonPolishedAssembly
    type: File
    format: edam:format_1929  # FASTA
    outputBinding:
      glob: $(inputs.output).fasta
  - id: pilonPolishedAssemblyChanges
    type: File
    outputBinding:
      glob: $(inputs.output).changes

#baseCommand: [java,org.broadinstitute.pilon.Pilon]
baseCommand: [java,com.simontuffs.onejar.Boot]
#stdout: out
hints:
  SoftwareRequirement:
    packages:
    - package: pilon
      version:
      - "1.22"
