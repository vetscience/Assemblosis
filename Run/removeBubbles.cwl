cwlVersion: v1.0
class: CommandLineTool
id: "removeBubbles"
doc: "Remove bubble contigs from assembled genome"

requirements:
  - class: ShellCommandRequirement
inputs:
  - id: contigs
    type: File
outputs:
  - id: assembly
    type: File
    outputBinding:
      glob: "filtered.$(inputs.contigs.basename)"
arguments:
 - shellQuote: false
   valueFrom: >
     awk '{if (($0~/^>/) && ($0~/suggestBubble=no/)) s=1; else if ($0~/^>/) s=0; if (s==1) print $0;}' ${inputs.contigs.path}
stdout: filtered.$(inputs.contigs.basename)
