cwlVersion: cwl:v1.0
class: ExpressionTool
inputs:
  masterFile:
    type: File
  indexFiles:
    type: File[]
outputs:
  hybridFile:
    type: File
expression: >
  ${
    var ret = inputs.masterFile;
    ret["secondaryFiles"] = inputs.indexFiles;
    return { "hybridFile": ret } ; }

