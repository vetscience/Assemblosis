cwlVersion: cwl:v1.0
class: ExpressionTool
requirements:
  - class: InitialWorkDirRequirement
    listing:
      - $(inputs.masterFile)
      - $(inputs.translation)
      - $(inputs.nsq)
      - $(inputs.nin)
      - $(inputs.nhr)
      - $(inputs.nog)
      - $(inputs.nni)
      - $(inputs.nnd)
inputs:
  masterFile:
    type: File
  translation: File
  nsq: File
  nin: File
  nhr: File
  nog: File
  nni: File
  nnd: File
outputs:
  hybridFile:
    type: File
expression: >
  ${
  var ret = inputs.masterFile;
  ret["secondaryFiles"] = [
      inputs.translation,
      inputs.nsq,
      inputs.nin,
      inputs.nhr,
      inputs.nog,
      inputs.nni,
      inputs.nnd,
  ];
  return { "hybridFile": ret } ; }
