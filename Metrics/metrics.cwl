cwlVersion: cwl:v1.0
class: Workflow
requirements:
  - class: InlineJavascriptRequirement
  - class: StepInputExpressionRequirement
  - class: ScatterFeatureRequirement
  - class: MultipleInputFeatureRequirement

inputs:
  reference: File
  assemblies: File[]
  labels: string[]
  threads: int
  minIdentity: float
  extensiveMisSize: int
  lineage: Directory
  buscoMode: string
  buscoName: string
  refGff: File

outputs:
  metrics:
    type: File
    outputSource: collectMetrics/table

steps:
  quastMetrics:
    run: quast.cwl
    in:
      reference: reference
      assembly: assemblies
      threads: threads
      minIdentity: minIdentity
      extensiveMisSize: extensiveMisSize
    out: [gageResult,quastResult,quastMisassemblies,quastSnpsZipped,icarusDir,icarusHtml,quastHtml,quastLog]
    scatter: [assembly]
    scatterMethod: dotproduct

  buscoMetrics:
    run: busco.cwl
    in:
      assembly: assemblies
      lineage: lineage
      mode: buscoMode
      outputName: buscoName
      threads: threads
    out: [buscoResult]
    scatter: [assembly]
    scatterMethod: dotproduct

  collectMetrics:
    run: collect.cwl
    in:
      labels: labels
      gageResults: quastMetrics/gageResult
      quastResults: quastMetrics/quastResult
      quastMisassemblies: quastMetrics/quastMisassemblies
      quastSnpsZipped: quastMetrics/quastSnpsZipped
      assemblies: assemblies
      refGff: refGff
      reference: reference
      buscoResults: buscoMetrics/buscoResult
    out: [table]
