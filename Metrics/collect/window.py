#!/usr/bin/env python

import os, sys, optparse
import numpy as np
from base import Base
from fasta import Fasta

#################################################
def options():
    parser = optparse.OptionParser('usage: python %prog -i filename -n size')
    parser.add_option('-i', '--snps', dest='snps', help='Nucmer', metavar='SNPS', default='')
    parser.add_option('-a', '--assembly', dest='assembly', help='FASTA assembly file', metavar='ASSEMBLY', default='')
    parser.add_option('-r', '--reference', dest='reference', help='FASTA reference file', metavar='REFERENCE', default='')
    parser.add_option('-n', '--size', dest='size', help='Window size (default=10000)', metavar='SIZE', default='10000')
    parser.add_option('-g', '--gaps', dest='gaps', help='Gaps file from Quast', metavar='GAPS', default='')
    parser.add_option('-R', '--reps', dest='reps', help='Predicted repeat regions (GFF format)', metavar='REPS', default='')
    parser.add_option('-G', '--gff', dest='gff', help='Coding regions', metavar='GFF', default='')
    parser.add_option('-m', '--misasm', dest='misasm', help='Misassemblies file from Quast', metavar='MISASM', default='')
    parser.add_option('-c', '--coords', dest='coords', help='Filtered nucmer coordinates file from Quast', metavar='COORDS', default='')
    parser.add_option('-P', '--pacbio', dest='pacbio', help='PacBio mpileup file', metavar='PACBIO', default='')
    parser.add_option('-I', '--illu', dest='illu', help='Illumina mpileup file', metavar='ILLUMINA', default='')
    parser.add_option('-b', '--binary', dest='binary', action='store_true', help='Consider all 100 regions either 1 or 0', default=False)
    options, args = parser.parse_args()
    return options


#################################################
def main():
    '''
    '''
    opts = options()

    size = int(opts.size)
    ref, asm = Fasta(opts.reference), Fasta(opts.assembly)
    dTransLoc, dReLoc, dInv, dCoords = {}, {}, {}, {}
    dTransLocCoords, dReLocCoords, dInvCoords = {}, {}, {}
    dRefLens, dStarts, dEnds, dRefs, dGaps = {}, {}, {}, {}, {}
    for i in xrange(len(ref.headers)):
        scafId = ref.headers[i].split(",")[0].replace(" ", "_")
        dRefs[scafId] = ref.seqs[i]
        print scafId
        dRefLens[scafId] = len(ref.seqs[i])
        dStarts[scafId] = dRefLens[scafId]
        dEnds[scafId] = 0
        dGaps[scafId] = []
        dTransLocCoords[scafId] = []
        dReLocCoords[scafId] = []
        dInvCoords[scafId] = []


    # Convert assembly coordinates to reference coordinates on misassebmlies
    ctgId = None
    with open(opts.misasm) as handle:
        for line in handle:
            items = line.strip().split()
            if len(items) == 1:
                ctgId = items[0]
            else:
                s1, e1, s2, e2 = int(items[-5]), int(items[-4]), int(items[-2]), int(items[-1])
                d1, d2 = abs(e1 - s1), abs(e2 - s2)
                if d2 < d1: s1, e1 = s2, e2
                if "translocation" in line:
                    try:
                        dTransLoc[ctgId].append((s1, e1))
                    except KeyError:
                        dTransLoc[ctgId] = []
                        dTransLoc[ctgId].append((s1, e1))
                elif "relocation" in line:
                    try:
                        dReLoc[ctgId].append((s1, e1))
                    except KeyError:
                        dReLoc[ctgId] = []
                        dReLoc[ctgId].append((s1, e1))
                elif "inversion" in line:
                    try:
                        dInv[ctgId].append((s1, e1))
                    except KeyError:
                        dInv[ctgId] = []
                        dInv[ctgId].append((s1, e1))
    dCoords = {} # use only start coordinate because stop coordinate does not always match
    with open(opts.coords) as handle:
        handle.readline()
        handle.readline()
        for line in handle:
            items = [item.strip() for item in line.strip().split("|")]
            scafId = items[-1].split()[0] # Reference id
            ctgId = items[-1].split()[1] # Assembly id
            sAsm = int(items[1].split()[0])
            try:
                dCoords[ctgId][sAsm] = (scafId, items[0], items[1])
            except KeyError:
                dCoords[ctgId] = {}
                dCoords[ctgId][sAsm] = (scafId, items[0], items[1])
    for key in dCoords:
        try:
            dTransLoc[key]
            for s, e in dTransLoc[key]:
                try:
                    refCoords = [int(item) for item in dCoords[key][s][1].split()]
                    scafId = dCoords[key][s][0].split("__")[0]
                    dTransLocCoords[scafId].append(refCoords)
                except KeyError:
                    pass
        except KeyError:
            print "# %s does not have translocations" %key
        try:
            dReLoc[key]
            for s, e in dReLoc[key]:
                try:
                    refCoords = [int(item) for item in dCoords[key][s][1].split()]
                    scafId = dCoords[key][s][0].split("__")[0]
                    dReLocCoords[scafId].append(refCoords)
                except KeyError:
                    pass
        except KeyError:
            print "# %s does not have relocations" %key
        try:
            dInv[key]
            for s, e in dInv[key]:
                try:
                    refCoords = [int(item) for item in dCoords[key][s][1].split()]
                    scafId = dCoords[key][s][0].split("__")[0]
                    dInvCoords[scafId].append(refCoords)
                except KeyError:
                    pass
        except KeyError:
            print "# %s does not have inversions" %key
            
                    
    # Map reference scaffolds ids to contig ids from the assembly
    dMapScafs = {}
    with open(opts.reps) as handle:
        for line in handle:
            if line[0] == "#": continue
            items = line.strip().split('\t')
            dMapScafs[items[0]] = True
    dReps, dGff = {}, {}
    for key in dRefLens:
        dReps[key] = []
        dGff[key] = []
        for tgt in dMapScafs:
            if tgt in key:
                dMapScafs[tgt] = key
                break

    with open(opts.reps) as handle:
        for line in handle:
            if line[0] == "#": continue
            items = line.strip().split('\t')
            scafId, start, end, motif = items[0], int(items[3]), int(items[4]), items[8]
            motif = motif.split()[1].strip('"')[6:]
            dReps[dMapScafs[scafId]].append((start, end, motif))

    with open(opts.gff) as handle:
        for line in handle:
            if line[0] == "#": continue
            items = line.strip().split('\t')
            if items[2] == "CDS":
                scafId, start, end = items[0], int(items[3]), int(items[4])
                dGff[dMapScafs[scafId]].append((start, end))                        

    scafId = None
    with open(opts.gaps) as handle:
        for line in handle:
            items = line.strip().split()
            try:
                int(items[0])
                items = [int(item) for item in items]
            except ValueError:
                scafId = items[0].split("__")[0]
                continue
            dGaps[scafId].append((items[0], items[1]))

    dIndels, dSnps = {}, {}
    with open(opts.snps) as handle:
        for line in handle:
            items = line.strip().split("\t")
            items[2], items[5] = int(items[2]), int(items[5])
            scafId = items[0].split("__")[0]
            if dStarts[scafId] > items[2]:
                dStarts[scafId] = items[2]
            if dEnds[scafId] < items[2]:
                dEnds[scafId] = items[2]
            if (items[3] == "." and items[4] != ".") or (items[3] != "." and items[4] == "."): # indel
                try:
                    queryId, scafPos, queryPos, cnt = dIndels[scafId][-1]
                    if items[2] == scafPos or items[5] == queryPos:
                        cnt += 1
                        dIndels[scafId][-1] = (items[1], items[2], items[5], cnt)
                    else:
                        cnt = 1
                        dIndels[scafId].append((items[1], items[2], items[5], cnt))
                except KeyError:
                    dIndels[scafId] = []
                    dIndels[scafId].append((items[1], items[2], items[5], 1))
            if (items[3] != "." and items[4] != "."): # nucleotide difference
                try:
                    dSnps[scafId].append((items[1], items[2], items[5]))
                except KeyError:
                    dSnps[scafId] = []
                    dSnps[scafId].append((items[1], items[2], items[5]))


    #############################################################
    #############################################################
    dRes = {}
    for key in dRefLens:
       dRes[key] = []

    # Print out indels
    dSeqsIndels = {}
    for key in dRefLens:
       dSeqsIndels[key] = [0 for i in xrange(dRefLens[key])]
    for key in dIndels:
       for items in dIndels[key]:
           queryId, scafPos, queryPos, cnt = items
           if opts.binary == True:
               dSeqsIndels[key][scafPos] += 1
           else:
               dSeqsIndels[key][scafPos] += cnt
    for key in dSeqsIndels:
       indels = []
       cnt = 0
       while cnt + size < len(dSeqsIndels[key]):
           indelCnt = 0
           for item in dSeqsIndels[key][cnt:(cnt + size)]:
               indelCnt += item
           indels.append(indelCnt)
           cnt += size / 2
       dRes[key].append(indels)

    # Print out nucleotide differences
    dSeqsSnps = {}
    for key in dRefLens:
       dSeqsSnps[key] = [0 for i in xrange(dRefLens[key])]
    for key in dSnps:
       for items in dSnps[key]:
           queryId, scafPos, queryPos = items
           dSeqsSnps[key][scafPos] += 1
    for key in dSeqsSnps:
       snps = []
       cnt = 0
       while cnt + size < len(dSeqsSnps[key]):
           snpCnt = 0
           for item in dSeqsSnps[key][cnt:(cnt + size)]:
               snpCnt += item
           snps.append(snpCnt)
           cnt += size / 2
       dRes[key].append(snps)

    # Print out aligned bits
    dSeqs = {}
    for key in dRefLens:
       dSeqs[key] = [0 for i in xrange(dRefLens[key])]
    for key in dStarts:
       startPos, endPos = dStarts[key], dEnds[key]
       for i in xrange(startPos, endPos):
           dSeqs[key][i] = 1
    for key in dSeqs:
       aligned = []
       cnt = 0
       while cnt + size < len(dSeqs[key]):
           alignedCnt = 0
           for item in dSeqs[key][cnt:(cnt + size)]:
               if item > 0: alignedCnt += item
           aligned.append(alignedCnt)
           cnt += size / 2
       dRes[key].append(aligned)

    # Print out GC content
    for key in dRefs:
       gcs = []
       cnt = 0
       while cnt + size < len(dSeqs[key]):
           gc = 0
           for item in dRefs[key][cnt:(cnt + size)]:
               if item == "c" or item == "C" or item == "g" or item == "G":
                   gc += 1
           gc = float(gc) * 100.0 / float(size)
           gcs.append(gc)
           cnt += size / 2
       dRes[key].append(gcs)

    # Print out gaps
    dSeqs = {}
    for key in dRefLens:
       dSeqs[key] = [0 for i in xrange(dRefLens[key])]
    for key in dGaps:
       for item in dGaps[key]:
           for i in xrange(item[0], item[1]):
               dSeqs[key][i] = 1
    for key in dSeqs:
       gaps = []
       cnt = 0
       while cnt + size < len(dSeqs[key]):
           gapsCnt = 0
           for item in dSeqs[key][cnt:(cnt + size)]:
               if item > 0: gapsCnt += item
           gaps.append(gapsCnt)
           cnt += size / 2
       dRes[key].append(gaps)

    # Print out repeat regions
    dSeqsReps = {}
    for key in dRefLens:
       dSeqsReps[key] = [0 for i in xrange(dRefLens[key])]
    for key in dReps:
       for item in dReps[key]:
           for i in xrange(item[0], item[1]):
               dSeqsReps[key][i] = 1
    for key in dSeqsReps:
       reps = []
       cnt = 0
       while cnt + size < len(dSeqsReps[key]):
           repsCnt = 0
           for item in dSeqsReps[key][cnt:(cnt + size)]:
               repsCnt += item
           reps.append(repsCnt)
           cnt += size / 2
       dRes[key].append(reps)

    # Print out coding regions
    dSeqs = {}
    for key in dRefLens:
       dSeqs[key] = [0 for i in xrange(dRefLens[key])]
    for key in dGff:
       for item in dGff[key]:
           for i in xrange(item[0], item[1]):
               dSeqs[key][i] = 1
    for key in dSeqs:
       gene = []
       cnt = 0
       while cnt + size < len(dSeqs[key]):
           geneCnt = 0
           for item in dSeqs[key][cnt:(cnt + size)]:
               geneCnt += item
           gene.append(geneCnt)
           cnt += size / 2
       dRes[key].append(gene)

    # Print out other non-coding regions
    dSeqsOther = {}
    for key in dRefLens:
       dSeqsOther[key] = [1 for i in xrange(dRefLens[key])]
    for key in dReps:
       for item in dReps[key]:
           for i in xrange(item[0], item[1]):
               dSeqsOther[key][i] = 0
    for key in dGff:
       for item in dGff[key]:
           for i in xrange(item[0], item[1]):
               dSeqsOther[key][i] = 0
    for key in dSeqsOther:
       others = []
       cnt = 0
       while cnt + size < len(dSeqsOther[key]):
           otherCnt = 0
           for item in dSeqsOther[key][cnt:(cnt + size)]:
               otherCnt += item
           others.append(otherCnt)
           cnt += size / 2
       dRes[key].append(others)

    # Print out translocated regions
    dSeqs = {}
    for key in dRefLens:
       dSeqs[key] = [0 for i in xrange(dRefLens[key])]
    for key in dTransLocCoords:
       for item in dTransLocCoords[key]:
           if item[1] < item[0]: item[0], item[1] = item[1], item[0]
           for i in xrange(item[0], item[1]):
               dSeqs[key][i] = 1
    for key in dSeqs:
       coords = []
       cnt = 0
       print "tr", key, len(dSeqs[key]), sum(dSeqs[key])
       while cnt + size < len(dSeqs[key]):
           coordsCnt = 0
           for item in dSeqs[key][cnt:(cnt + size)]:
               coordsCnt += item
           coords.append(coordsCnt)
           cnt += size / 2
       dRes[key].append(coords)

    # Print out relocated regions
    dSeqs = {}
    for key in dRefLens:
       dSeqs[key] = [0 for i in xrange(dRefLens[key])]
    for key in dReLocCoords:
       for item in dReLocCoords[key]:
           if item[1] < item[0]: item[0], item[1] = item[1], item[0]
           for i in xrange(item[0], item[1]):
               dSeqs[key][i] = 1
    for key in dSeqs:
       coords = []
       cnt = 0
       print "re", key, len(dSeqs[key]), sum(dSeqs[key])
       while cnt + size < len(dSeqs[key]):
           coordsCnt = 0
           for item in dSeqs[key][cnt:(cnt + size)]:
               coordsCnt += item
           coords.append(coordsCnt)
           cnt += size / 2
       dRes[key].append(coords)

    # Print out inverted regions
    dSeqs = {}
    for key in dRefLens:
       dSeqs[key] = [0 for i in xrange(dRefLens[key])]
    for key in dInvCoords:
       for item in dInvCoords[key]:
           if item[1] < item[0]: item[0], item[1] = item[1], item[0]
           for i in xrange(item[0], item[1]):
               dSeqs[key][i] = 1
    for key in dSeqs:
       coords = []
       cnt = 0
       print "iv", key, len(dSeqs[key]), sum(dSeqs[key])
       while cnt + size < len(dSeqs[key]):
           coordsCnt = 0
           for item in dSeqs[key][cnt:(cnt + size)]:
               coordsCnt += item
           coords.append(coordsCnt)
           cnt += size / 2
       dRes[key].append(coords)

    # Print out PacBio mapping depth
    dSeqs = {}
    for key in dRefLens:
       dSeqs[key] = [0 for i in xrange(dRefLens[key])]
    with open(opts.pacbio) as handle:
        for line in handle:
            items = line.strip().split()
            scafId, pos, depth = items[0], int(items[1]), int(items[2])
            dSeqs[dMapScafs[scafId]][pos-1] = depth
    for key in dSeqs:
       coords = []
       cnt = 0
       while cnt + size < len(dSeqs[key]):
           coordsCnt = 0
           for item in dSeqs[key][cnt:(cnt + size)]:
               coordsCnt += item
           coords.append(coordsCnt)
           cnt += size / 2
       dRes[key].append(coords)

    # Print out Illumina mapping depth
    dSeqs = {}
    for key in dRefLens:
       dSeqs[key] = [0 for i in xrange(dRefLens[key])]
    with open(opts.illu) as handle:
        for line in handle:
            items = line.strip().split()
            scafId, pos, depth = items[0], int(items[1]), int(items[2])
            dSeqs[dMapScafs[scafId]][pos-1] = depth
    for key in dSeqs:
       coords = []
       cnt = 0
       while cnt + size < len(dSeqs[key]):
           coordsCnt = 0
           for item in dSeqs[key][cnt:(cnt + size)]:
               coordsCnt += item
           coords.append(coordsCnt)
           cnt += size / 2
       dRes[key].append(coords)

    # Print out PacBio low mapping regions
    dSeqs = {}
    for key in dRefLens:
       dSeqs[key] = [0 for i in xrange(dRefLens[key])]
    with open(opts.pacbio) as handle:
        for line in handle:
            items = line.strip().split()
            scafId, pos, depth = items[0], int(items[1]), int(items[2])
            dSeqs[dMapScafs[scafId]][pos-1] = depth
    for key in dSeqs:
       coords = []
       cnt = 0
       while cnt + size < len(dSeqs[key]):
           coordsCnt = 0
           for item in dSeqs[key][cnt:(cnt + size)]:
               if item <= 5: coordsCnt += 1
           coords.append(coordsCnt)
           cnt += size / 2
       dRes[key].append(coords)

    # Print out Illumina low mapping regions
    dSeqs = {}
    for key in dRefLens:
       dSeqs[key] = [0 for i in xrange(dRefLens[key])]
    with open(opts.illu) as handle:
        for line in handle:
            items = line.strip().split()
            scafId, pos, depth = items[0], int(items[1]), int(items[2])
            dSeqs[dMapScafs[scafId]][pos-1] = depth
    for key in dSeqs:
       coords = []
       cnt = 0
       while cnt + size < len(dSeqs[key]):
           coordsCnt = 0
           for item in dSeqs[key][cnt:(cnt + size)]:
               if item <= 5: coordsCnt += 1
           coords.append(coordsCnt)
           cnt += size / 2
       dRes[key].append(coords)

    # Print the matrix
    for key in sorted(dRes):
        with open("%s.txt" %key, "w") as handle:
            labels = ["Indels","Nucleotide differences","Alignment","GC content","Gaps", "Repeats", "Coding regions", "Non-coding non-repeat regions", "Translocations", "Relocations", "Inversions","PacBio mapping depth","Illumina mapping depth","PacBio low mapping regions","Illumina low mapping regions"]
            cnt = 0
            for items in dRes[key]:
                handle.write("%s\t%s\n" %(labels[cnt], "\t".join([str(item) for item in items])))
                cnt += 1

#################################################
if __name__ == "__main__":
    main()
