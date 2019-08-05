cwlVersion: cwl:v1.0
class: Workflow
requirements:
  - "$import": assembly-typedef.yml
  - class: InlineJavascriptRequirement
  - class: StepInputExpressionRequirement
  - class: ScatterFeatureRequirement
  - class: MultipleInputFeatureRequirement

inputs:
  pacBioDataDir: Directory
  pacBioInBam: boolean
  prefix: string
  genomeSize: string
  minReadLen: int
  corMaxEvidenceErate: float
  readsPe1:
    type: File[]
  readsPe2:
    type: File[]
  phredsPe:
    type: string[]
  slidingWindow: assembly-typedef.yml#slidingWindow
  illuminaClip: assembly-typedef.yml#illuminaClipping?
  leading: int
  trailing: int
  minlen: int
  threads: int
  orientation: string
  maxFragmentLens: int[]
  polishedAssembly: string
  diploidOrganism: boolean
  fix: string
  database: Directory
  taxons:
    type: int[]
  partialMatch: int
  repBaseLibrary: File
  noInterspersed: boolean[]
  noLowComplexity: boolean[]

outputs:
  correctedReads:
    type: File
    outputSource: correct/correctedReads
  trimmedReads:
    type: File
    outputSource: assemble/trimmedReads
  canuAssembly:
    type: File
    outputSource: assemble/assembly
  arrowAssembly:
    type: File
    outputSource: arrow/arrowPolishedAssembly
  pilonAssembly:
    type: File
    outputSource: pilon/pilonPolishedAssembly
  trimmedReadFiles1:
    type: File[]
    outputSource: cleanIlluminaReads/trimmedPe1
  trimmedReadFiles2:
    type: File[]
    outputSource: cleanIlluminaReads/trimmedPe2
  sortedBamIndexFileOut:
    type: File[]
    outputSource: expressionToolBam/hybridFile
  deconReport:
    type: File
    outputSource: classifyReads/report
  deconClassification:
    type: File
    outputSource: classifyReads/classification
  decontaminatedReads:
    type: File
    outputSource: decontaminate/deconReads
  contaminatedReads:
    type: File
    outputSource: decontaminate/conReads
  assemblyMasked:
    type: File
    outputSource: combineCatFiles/maskedAssembly
  assemblyMerged:
    type: File
    outputSource: haploMerge/mergedAssembly

steps:
  cleanIlluminaReads:
    run: trimmomaticpe.cwl
    in:
      phred: phredsPe
      threads: threads
      reads1: readsPe1
      reads2: readsPe2
      slidingWindow: slidingWindow
      illuminaClip: illuminaClip
      leading: leading
      trailing: trailing
      minlen: minlen
    out: [trimmedPe1, trimmedPe2, trimmedUnpe1, trimmedUnpe2, trimLogFile]
    scatter: [reads1, reads2, phred]
    scatterMethod: dotproduct

  hdf5check:
    run: hdf5check.cwl
    in:
      directory: pacBioDataDir
      fastq: pacBioInBam
    out: [pbFastqReads]

  correct:
    run: canuCorrect.cwl
    in:
      prefix: prefix
      genomeSize: genomeSize
      pacbio-raw: hdf5check/pbFastqReads
      corMaxEvidenceErate: corMaxEvidenceErate
      minThreads: threads
      maxThreads: threads
    out: [correctedReads]

#  trim:
#    run: canuTrim.cwl
#    in:
#      prefix: prefix
#      genomeSize: genomeSize
#      minReadLen: minReadLen
#      pacbio-corrected: correct/correctedReads
#      corMaxEvidenceErate: corMaxEvidenceErate
#      minThreads: threads
#      maxThreads: threads
#    out: [trimmedReads]

  renameReads:
    run: renameReads.cwl
    in:
      trimmedReads: correct/correctedReads
    out: [renamedReads, mappedIds]

  classifyReads:
    run: centrifuge.cwl
    in:
      database: database
      trimmedReads: renameReads/renamedReads
      threads: threads
      partialMatch: partialMatch
    out: [report, classification]

  decontaminate:
    run: decon.cwl
    in:
      prefix: prefix
      trimmedReads: renameReads/renamedReads
      taxons: taxons
      classificationFile: classifyReads/classification
      mappedIds: renameReads/mappedIds
      partialMatch: partialMatch
    out: [deconReads, conReads]

  assemble:
    run: canuAssemble.cwl
    in:
      prefix: prefix
      genomeSize: genomeSize
      minReadLen: minReadLen
      pacbio-corrected: decontaminate/deconReads
      corMaxEvidenceErate: corMaxEvidenceErate
      minThreads: threads
      maxThreads: threads
    out: [trimmedReads, assembly]

  arrow:
    run: arrow.cwl
    in:
      dataDir: pacBioDataDir
      assembly: assemble/assembly
      prefix: prefix
      bam: pacBioInBam
    out: [arrowPolishedAssembly]

  indexReference:
    run: bowtie2-build.cwl
    in:
      reference: arrow/arrowPolishedAssembly
    out: [indexFiles]

  expressionToolBowtie:
    run: expressiontool.cwl
    in:
      masterFile:
          source: arrow/arrowPolishedAssembly
      indexFiles:
          source: indexReference/indexFiles
    out: [hybridFile]

  mapIlluminaReads:
    run: bowtie2.cwl
    in:
      phred: phredsPe
      orientation: orientation
      maxFragmentLen: maxFragmentLens
      threads: threads
      reference: expressionToolBowtie/hybridFile
      reads1: cleanIlluminaReads/trimmedPe1
      reads2: cleanIlluminaReads/trimmedPe2
    out: [samFile]
    scatter: [phred, reads1, reads2, maxFragmentLen]
    scatterMethod: dotproduct

  sortMappedReads:
    run: samsort.cwl
    in:
      threads: threads
      inputSamFile: mapIlluminaReads/samFile
    out: [sortedBamFile]
    scatter: inputSamFile

  indexBamFile:
    run: samindex.cwl
    in:
      inputBamFile: sortMappedReads/sortedBamFile
    out: [bamIndexFile]
    scatter: inputBamFile

  expressionToolBam:
    run: expressiontool.cwl
    in:
      masterFile:
          source: sortMappedReads/sortedBamFile
      indexFiles:
          source: [indexBamFile/bamIndexFile]
    out: [hybridFile]
    scatter: [masterFile, indexFiles]
    scatterMethod: dotproduct

  pilon:
    run: pilon.cwl
    in:
      bamPe: expressionToolBam/hybridFile
      reference: arrow/arrowPolishedAssembly
      output: polishedAssembly
      diploidOrganism: diploidOrganism
      fix: fix
    out: [pilonPolishedAssembly, pilonPolishedAssemblyChanges]

  indexAssembly:
    run: indexassembly.cwl
    in:
      scaffolds: pilon/pilonPolishedAssembly
    out: [indexFiles]

  expressionToolRepeatModeler:
    run: expressiontool.cwl
    in:
      masterFile:
          source: pilon/pilonPolishedAssembly
      indexFiles:
          source: indexAssembly/indexFiles
    out: [hybridFile]

  inferRepeats:
    run: repeatmodeler.cwl
    in:
      repBaseLibrary: repBaseLibrary
      threads: threads
      database: expressionToolRepeatModeler/hybridFile
    out: [repeatFastaFile, repeatLibrary]

  maskRepeats:
    run: repeatmasker.cwl
    in:
      threads: threads
      noInterspersed: noInterspersed
      noLowComplexity: noLowComplexity
      repeatLibrary: [inferRepeats/repeatFastaFile, inferRepeats/repeatLibrary, inferRepeats/repeatLibrary]
      reference: pilon/pilonPolishedAssembly
    out: [categoryFile]
    scatter: [noInterspersed, noLowComplexity, repeatLibrary]
    scatterMethod: dotproduct

  combineCatFiles:
    run: combinecats.cwl
    in:
      assembly: pilon/pilonPolishedAssembly
      categories: maskRepeats/categoryFile
    out: [maskedAssembly]

  haploMerge:
    run: haplomerger.cwl
    in:
      assembly: pilon/pilonPolishedAssembly
      maskedAssembly: combineCatFiles/maskedAssembly
      trimmedReads: decontaminate/deconReads
      threads: threads
    out: [mergedAssembly, scoreMatrix]
