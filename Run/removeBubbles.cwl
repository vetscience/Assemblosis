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
     awk '{ if ((NR>1)&&($0~/^>/)) printf("\\n%s", $0); else if (NR==1) printf("%s", $0); else printf("\\t%s", $0); }' $(inputs.contigs.path) |
     grep -F suggestBubble=no - |
     tr "\\t" "\\n"
stdout: filtered.$(inputs.contigs.basename)
