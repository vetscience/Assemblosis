#!/usr/bin/env python

import os, sys, optparse, gzip

#################################################
def options():
    parser = optparse.OptionParser('usage: python %prog -i filename -n size')
    parser.add_option('-i', '--gff', dest='gff', help='GFF file for reference', metavar='GFF', default='')
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
    dScafs = {}
    with open(opts.gff) as handle:
        for line in handle:
            if line[0] == '#': continue
            items = line.strip().split('\t')
            if items[2] == "CDS":
                scafId, start, end, phase = items[0], int(items[3]), int(items[4]), int(items[7])
                mRnaId = items[8].split(';')[1].replace('Parent=','')
                if start > end: start, end = end, start
                try:
                    dScafs[scafId].append((start, end, phase, mRnaId))
                except KeyError:
                    dScafs[scafId] = []
                    dScafs[scafId].append((start, end, phase, mRnaId))

    lines = []
    prevInsLine, prevDelLine, prevInsIdx, prevDelIdx = None, None, None, None
    with gzip.open(opts.snps) as handle:
        for line in handle:
            items = line.strip().split('\t')
            scafId1, scafId2, pos1, pos2 = items[0], items[1], int(items[2]), int(items[5])
            insertion, deletion = False, False
            if items[3] == ".": insertion = True
            if items[4] == ".": deletion = True
            if insertion == True:
                if prevDelIdx != None:
                    lines.append(prevDelLine)
                    prevDelLine, prevDelIdx = None, None
                if prevInsIdx != None:
                    if prevInsIdx != items[2]:
                        lines.append(prevInsLine)
                prevInsIdx, prevInsLine = items[2], line.strip()
            elif deletion == True:
                if prevInsIdx != None:
                    lines.append(prevInsLine)
                    prevInsLine, prevInsIdx = None, None
                if prevDelIdx != None:
                    if prevDelIdx != items[5]:
                        lines.append(prevDelLine)
                prevDelIdx, prevDelLine = items[5], line.strip()
            else:
                if prevDelIdx != None:
                    lines.append(prevDelLine)
                    prevDelLine, prevDelIdx = None, None
                if prevInsIdx != None:
                    lines.append(prevInsLine)
                    prevInsLine, prevInsIdx = None, None
                lines.append(line.strip())
    if prevInsIdx != None:
        lines.append(prevInsLine)
    if prevDelIdx != None:
        lines.append(prevDelLine)
    #for line in lines:
    #    print line

    cnt, indelCnt, totalCnt, totalIndelCnt = 0, 0, 0, 0
    dCdsCnt, dMrnaCnt = {}, {}
    indelMrnas = set()
    with open(opts.snps) as handle:
        for line in lines:
            #if line == None: continue
            totalCnt += 1
            items = line.strip().split('\t')
            scafId, pos = items[0], int(items[2])
            scafId = '_'.join(scafId.split("_")[:-2])
            indel = False
            if items[3] == "." or items[4] == ".":
                indel = True
                totalIndelCnt += 1
            try:
              for cds in dScafs[scafId]:
                start, end, phase, mRnaId = cds
                if pos >= start and pos <= end:
                    cnt += 1
                    if indel == True:
                        indelCnt += 1
                        indelMrnas.add("%s" %(mRnaId))
                    dCdsCnt["%s_%d_%d" %(scafId, start, end)] = 1
                    dMrnaCnt["%s_%s" %(scafId, mRnaId)] = 1
                    break
            except KeyError:
                pass
    print "%d\t%d\t%d\t%d\t%d\t%d\t%d" %(cnt - indelCnt, indelCnt, sum([dCdsCnt[key] for key in dCdsCnt]), sum([dMrnaCnt[key] for key in dMrnaCnt]), totalCnt - cnt, totalIndelCnt - indelCnt, totalCnt - cnt - totalIndelCnt + indelCnt)
    print >> sys.stderr, '\t'.join(sorted(indelMrnas))
    #print "%d SNPs and %d indels in %d CDSs in %d mRNAs, %d outside CDSs of which %d are indels and rest %d SNPs" %(cnt - indelCnt, indelCnt, sum([dCdsCnt[key] for key in dCdsCnt]), sum([dMrnaCnt[key] for key in dMrnaCnt]), totalCnt - cnt, totalIndelCnt - indelCnt, totalCnt - cnt - totalIndelCnt + indelCnt)


#################################################
if __name__ == "__main__":
    main()
