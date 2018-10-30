cwlVersion: v1.0
class: CommandLineTool
id: "busco"
doc: "Estimate the completeness of a genome using predicted genes"
requirements:
  - class: InlineJavascriptRequirement
  - class: EnvVarRequirement
    envDef:
      AUGUSTUS_CONFIG_PATH: /usr/local/config
inputs:
  - id: assembly
    type: File
    inputBinding:
      prefix: -i
      position: 1
  - id: lineage
    type: Directory
    inputBinding:
      prefix: -l
      position: 2
  - id: mode
    type: string
    default: geno
    inputBinding:
      prefix: -m
      position: 3
  - id: outputName
    type: string
    inputBinding:
      prefix: -o
      position: 4
  - id: threads
    type: int
    inputBinding:
      prefix: -c
      position: 5
  - id: blastSingleCore
    type: boolean
    default: true
    inputBinding:
      prefix: --blast_single_core
      position: 6
outputs:
  - id: buscoResult
    type: File
    outputBinding:
      glob: run_*/short_summary_*.txt
baseCommand: ["run_BUSCO.py", "-f"]
arguments: []
hints:
  - class: DockerRequirement
    dockerPull: quay.io/biocontainers/busco:3.0.2--py35_6
