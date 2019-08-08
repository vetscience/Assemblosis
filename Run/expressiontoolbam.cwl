cwlVersion: cwl:v1.0
class: ExpressionTool
requirements:
  - class: InitialWorkDirRequirement
    listing:
      - $(inputs.masterFile)
      - $(inputs.bai)
inputs:
  masterFile:
    type: File
  bai: File
outputs:
  hybridFile:
    type: File
expression: >
  ${
  var ret = inputs.masterFile;
  ret["secondaryFiles"] = [
      inputs.bai,
  ];
  return { "hybridFile": ret } ; }
