cwlVersion: cwl:v1.0
class: ExpressionTool
requirements:
  - class: InitialWorkDirRequirement
    listing:
      - $(inputs.masterFile)
      - $(inputs.bt2_1)
      - $(inputs.bt2_2)
      - $(inputs.bt2_3)
      - $(inputs.bt2_4)
      - $(inputs.bt2rev1)
      - $(inputs.bt2rev2)
inputs:
  masterFile:
    type: File
  bt2_1: File
  bt2_2: File
  bt2_3: File
  bt2_4: File
  bt2rev1: File
  bt2rev2: File
outputs:
  hybridFile:
    type: File
expression: >
  ${
  var ret = inputs.masterFile;
  ret["secondaryFiles"] = [
      inputs.bt2_1,
      inputs.bt2_2,
      inputs.bt2_3,
      inputs.bt2_4,
      inputs.bt2rev1,
      inputs.bt2rev2,
  ];
  return { "hybridFile": ret } ; }
