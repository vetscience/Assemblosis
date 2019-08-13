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
  pacBioTmpDir: string
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
  minThreads: int
  canuConcurrency: int
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
  trueValue: boolean
  falseValue: boolean

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
      minThreads: minThreads
      maxThreads: threads
      corConcurrency: canuConcurrency
    out: [correctedReads]

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
      minThreads: minThreads
      maxThreads: threads
      obtmhapConcurrency: canuConcurrency
      utgmhapConcurrency: canuConcurrency
      obtmmapConcurrency: canuConcurrency
      utgmmapConcurrency: canuConcurrency
      obtovlConcurrency: canuConcurrency
      utgovlConcurrency: canuConcurrency
    out: [trimmedReads, assembly]

  arrow:
    run: arrow.cwl
    in:
      dataDir: pacBioDataDir
      tmpDir: pacBioTmpDir
      assembly: assemble/assembly
      prefix: prefix
      bam: pacBioInBam
    out: [arrowPolishedAssembly]

  indexReference:
    run: bowtie2-build.cwl
    in:
      reference: arrow/arrowPolishedAssembly
    out: [referenceAssembly, bt2_1, bt2_2, bt2_3, bt2_4, bt2rev1, bt2rev2]

  expressionToolBowtie:
    run: expressiontoolbowtie.cwl
    in:
      masterFile:
        source: indexReference/referenceAssembly
      bt2_1: indexReference/bt2_1
      bt2_2: indexReference/bt2_2
      bt2_3: indexReference/bt2_3
      bt2_4: indexReference/bt2_4
      bt2rev1: indexReference/bt2rev1
      bt2rev2: indexReference/bt2rev2
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
    out: [sortedBamFile, bamIndexFile]
    scatter: inputBamFile

  expressionToolBam:
    run: expressiontoolbam.cwl
    in:
      masterFile:
          source: indexBamFile/sortedBamFile
      bai: indexBamFile/bamIndexFile
    out: [hybridFile]
    scatter: [masterFile, bai]
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
    out: [pilonPolishedAssembly, translation, nsq, nin, nhr, nog, nni, nnd]

  expressionToolRepeatModeler:
    run: expressiontoolrepeats.cwl
    in:
      masterFile:
          source: indexAssembly/pilonPolishedAssembly
      translation: indexAssembly/translation
      nsq: indexAssembly/nsq
      nin: indexAssembly/nin
      nhr: indexAssembly/nhr
      nog: indexAssembly/nog
      nni: indexAssembly/nni
      nnd: indexAssembly/nnd
    out: [hybridFile]

  inferRepeats:
    run: repeatmodeler.cwl
    in:
      repBaseLibrary: repBaseLibrary
      threads: threads
      database: expressionToolRepeatModeler/hybridFile
    out: [repeatFastaFile, repeatLibrary]

  maskCustomRepeats:
    run: repeatmasker.cwl
    in:
      threads: threads
      noInterspersed: falseValue
      noLowComplexity: trueValue
      repeatLibrary: inferRepeats/repeatFastaFile
      reference: pilon/pilonPolishedAssembly
    out: [categoryFile]

  maskTranspRepeats:
    run: repeatmasker.cwl
    in:
      threads: threads
      noInterspersed: falseValue
      noLowComplexity: trueValue
      repeatLibrary: inferRepeats/repeatLibrary
      reference: pilon/pilonPolishedAssembly
    out: [categoryFile]

  maskSimpleRepeats:
    run: repeatmasker.cwl
    in:
      threads: threads
      noInterspersed: trueValue
      noLowComplexity: falseValue
      repeatLibrary: inferRepeats/repeatLibrary
      reference: pilon/pilonPolishedAssembly
    out: [categoryFile]

  combineCatFiles:
    run: combinecats.cwl
    in:
      assembly: pilon/pilonPolishedAssembly
      categories: [maskCustomRepeats/categoryFile, maskTranspRepeats/categoryFile, maskSimpleRepeats/categoryFile]
    out: [maskedAssembly]

  haploMerge:
    run: haplomerger.cwl
    in:
      assembly: pilon/pilonPolishedAssembly
      maskedAssembly: combineCatFiles/maskedAssembly
      trimmedReads: decontaminate/deconReads
      threads: threads
    out: [mergedAssembly, scoreMatrix]
