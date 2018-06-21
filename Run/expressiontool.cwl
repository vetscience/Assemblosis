cwlVersion: cwl:v1.0
class: ExpressionTool
#requirements:
#  - class: EnvVarRequirement
#    envDef:
#      TMPDIR: /home/pakorhon/Images/Tmp
inputs:
  masterFile:
    type: File
    #format: http://edamontology.org/format_1929  # FASTA
  indexFiles:
    type: File[]
outputs:
  hybridFile:
    type: File
    #format: http://edamontology.org/format_1929  # FASTA
expression: >
  ${
    var ret = inputs.masterFile;
    ret["secondaryFiles"] = inputs.indexFiles;
    return { "hybridFile": ret } ; }

