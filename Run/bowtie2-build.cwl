cwlVersion: v1.0
class: CommandLineTool
id: "bowtie2-build"
doc: "Create a bowtie2 reference file"
requirements:
  - class: InlineJavascriptRequirement
#  - class: EnvVarRequirement
#    envDef:
#      TMPDIR: /home/pakorhon/Images/Tmp

inputs:
  - id: reference
    type: File
    #format: edam:format_1929  # fasta
    inputBinding:
      position: 1

arguments:
  - valueFrom: $(inputs.reference.basename)
    position: 2

outputs:
  - id: indexFiles
    type: File[]
    outputBinding:
      glob: $(inputs.reference.basename).*
#  - id: idxFile
#    type: ["null", File]
#    outputBinding:
#      glob: ref.$(inputs.reference.basename)
#    secondaryFiles:
#      - .1.bt2
#      - .2.bt2
#      - .3.bt2
#      - .4.bt2
#      - .rev.1.bt2
#      - .rev.2.bt2
#  - id: idxFile1
#    type: File
#    outputBinding:
#      glob: $(inputs.reference.basename).1.bt2
#  - id: idxFile2
#    type: File
#    outputBinding:
#      glob: $(inputs.reference.basename).2.bt2
#  - id: idxFile3
#    type: File
#    outputBinding:
#      glob: $(inputs.reference.basename).3.bt2
#  - id: idxFile4
#    type: File
#    outputBinding:
#      glob: $(inputs.reference.basename).4.bt2
#  - id: idxFileRev1
#    type: File
#    outputBinding:
#      glob: $(inputs.reference.basename).rev.1.bt2
#  - id: idxFileRev2
#    type: File
#    outputBinding:
#      glob: $(inputs.reference.basename).rev.2.bt2

baseCommand: [bowtie2-build]

#stdout: ref.$(inputs.reference.basename)

hints:
  SoftwareRequirement:
    packages:
    - package: bowtie2
      version:
      - "2.2.8"
