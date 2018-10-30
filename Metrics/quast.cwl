cwlVersion: v1.0
class: CommandLineTool
id: "quast"
doc: "Compare the assembly against the reference genome"
requirements:
  - class: InlineJavascriptRequirement
inputs:
  - id: assembly
    type: File
    inputBinding:
      position: 1
  - id: reference
    type: File
    inputBinding:
      position: 2
      prefix: -R
  - id: gffFile
    type: File?
    inputBinding:
      position: 3
      prefix: -G
  - id: bamFile
    type: File?
    inputBinding:
      prefix: --bam
      position: 4
  - id: threads
    type: int?
    inputBinding:
      prefix: -t
      position: 5
  - id: gage
    type: boolean?
    default: true
    inputBinding:
      prefix: --gage
      position: 6
  - id: minIdentity
    type: float
    default: 98.0
    inputBinding:
      prefix: --min-identity
      position: 7
  - id: extensiveMisSize
    type: int
    default: 1000
    inputBinding:
      prefix: --extensive-mis-size
      position: 8
  - id: ambiguity
    type: string
    default: one
    inputBinding:
      prefix: --ambiguity-usage
      position: 9
  - id: plotFormat
    type: string
    default: svg
    inputBinding:
      prefix: --plots-format
      position: 10
  - id: eukaryote
    type: boolean
    default: true
    inputBinding:
      prefix: --eukaryote
      position: 11
outputs:
  - id: gageResult
    type: File
    outputBinding:
      glob: "quast_results/latest/gage_report.txt"
#      glob: quast_results/latest/gage/gage_*.stdout
  - id: quastResult
    type: File
    outputBinding:
      glob: "quast_results/latest/report.txt"
  - id: quastMisassemblies
    type: File
    outputBinding:
      glob: "quast_results/latest/contigs_reports/misassemblies_report.txt"
  - id: quastSnpsZipped
    type: File
    outputBinding:
      glob: "quast_results/latest/contigs_reports/nucmer_output/*.used_snps.gz"
  - id: icarusDir
    type: Directory
    outputBinding:
      glob: "quast_results/latest/icarus_viewers"
  - id: icarusHtml
    type: File
    outputBinding:
      glob: "quast_results/latest/icarus.html"
  - id: quastHtml
    type: File
    outputBinding:
      glob: "quast_results/latest/report.html"
  - id: quastLog
    type: File
    outputBinding:
      glob: "quast_results/latest/quast.log"
baseCommand: ["quast"]
arguments: []
hints:
  SoftwareRequirement:
    packages:
    - package: quast
      version:
      - "4.6.3"