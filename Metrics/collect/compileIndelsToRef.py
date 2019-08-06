#!/usr/bin/env python

import os, sys, optparse, gzip
from fasta import Fasta

#################################################
def options():
    parser = optparse.OptionParser('usage: python %prog -i filename -n size')
    parser.add_option('-i', '--fasta', dest='fasta', help='FASTA reference', metavar='FASTA', default='')
    parser.add_option('-g', '--gff', dest='gff', help='GFF reference', metavar='GFF', default='')
    parser.add_option('-n', '--snps', dest='snps', help='Nucleotide differences', metavar='SNPS', default='')
    #parser.add_option('-r', '--order', dest='order', action='store_true', help='Longest first (default=FALSE)', default=False)
    #parser.add_option('-a', '--assemble', dest='assemble', action='store_true', help='Do assembly', default=False)
    options, args = parser.parse_args()
    #if options.fasta == '':
    #    parser.print_help()
    #    sys.exit(1)
    return options


#################################################
def main():
    '''
    '''
    opts = options()
    dGff = {}
    with open(opts.gff) as handle:
        for line in handle:
            if line[0] == '#' or len(line) <= 1: continue
            items = line.strip().split('\t')
            if items[2] == "CDS":
                scafId, start, end, phase = items[0], int(items[3]), int(items[4]), int(items[7])
                mRnaId = items[8].split(';')[1].replace('Parent=','')
                if start > end: start, end = end, start
                try:
                    dGff[scafId].append((start, end, phase, mRnaId))
                except KeyError:
                    dGff[scafId] = []
                    dGff[scafId].append((start, end, phase, mRnaId))

    dScafs = {}
    fasta = Fasta(opts.fasta)
    for i in xrange(len(fasta.headers)):
        header = fasta.headers[i].split()[0]
        dScafs[header] = [nt.upper() for nt in fasta.seqs[i]]

    prevScafInsId, prevScafDelId, prevInsIdx, prevDelIdx = None, None, None, None
    insCnt, delCnt = 1, 1
    insFrameCnt, delFrameCnt = 0, 0
    allInsCnt, allDelCnt = 0, 0
    with gzip.open(opts.snps) as handle:
        for line in handle:
            items = line.strip().split('\t')
            scafId, pos = items[0], int(items[2])
            scafId = '_'.join(scafId.split("_")[:-2])
            insertion, deletion = False, False
            if items[3] == ".": insertion = True
            if items[4] == ".": deletion = True
            if insertion == True:
                if prevInsIdx != None:
                    if prevInsIdx == items[2]:
                        insCnt += 1
                    else:
                        try:
                          if insCnt % 3 == 0:
                           for item in dGff[prevScafInsId]:
                               start, end, phase, mRnaId = item
                               if int(prevInsIdx) >= start and int(prevInsIdx) <=end:
                                   insFrameCnt += 1
                                   allInsCnt += 1
                                   break
                          elif prevScafInsId != None:
                           for item in dGff[prevScafInsId]:
                               start, end, phase, mRnaId = item
                               if int(prevInsIdx) >= start and int(prevInsIdx) <=end:
                                   allInsCnt += 1
                                   break
                        except KeyError:
                          pass
                        prevInsIdx, insCnt = None, 1
                prevInsIdx, prevScafInsId = items[2], scafId
            if deletion == True:
                if prevDelIdx != None:
                    if prevDelIdx == items[5]:
                        delCnt += 1
                    else:
                        try:
                          if delCnt % 3 == 0:
                           for item in dGff[prevScafDelId]:
                               start, end, phase, mRnaId = item
                               if int(prevDelIdx) >= start and int(prevDelIdx) <=end:
                                   delFrameCnt += 1
                                   allDelCnt += 1
                                   break
                          elif prevScafDelId != None:
                           for item in dGff[prevScafDelId]:
                               start, end, phase, mRnaId = item
                               if int(prevDelIdx) >= start and int(prevDelIdx) <=end:
                                   allDelCnt += 1
                                   break
                        except KeyError:
                          pass
                        prevDelIdx, delCnt = None, 1
                prevDelIdx, prevScafDelId = items[5], scafId
    print insFrameCnt, delFrameCnt, insFrameCnt + delFrameCnt
    print allInsCnt, allDelCnt, allInsCnt + allDelCnt
            

#################################################
if __name__ == "__main__":
    main()
