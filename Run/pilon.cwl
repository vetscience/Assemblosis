cwlVersion: v1.0
class: CommandLineTool
id: "pilon"
doc: "Polishing an assembly using Illumina reads"
requirements:
  - class: InlineJavascriptRequirement
  - class: EnvVarRequirement
    envDef:
      CLASSPATH: /usr/local/share/pilon-1.22-0/pilon-1.22.jar
 
inputs:
  - id: reference
    type: File
    inputBinding:
      prefix: --genome
      position: 1
  - id: bamPe
    type: File[]
    secondaryFiles:
      - .bai
  - id: output
    type: string
    inputBinding:
      prefix: --output
      position: 3
  - id: diploidOrganism
    type: boolean
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
    default: true
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

baseCommand: [java,com.simontuffs.onejar.Boot]
hints:
  - class: DockerRequirement
    dockerPull: quay.io/biocontainers/pilon:1.22--py36_0
