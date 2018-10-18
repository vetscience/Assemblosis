#!/usr/bin/env python

import sys
from base import Base

class Gff(Base):
    '''
    '''
    
    def __init__(self, filename = None, postfix = None):
        '''
        '''
        self.version = None
        self.filename = filename
        self.lines = None
        self.postfix = None
        if filename != None:
            self._parse()


    def _parse(self):
        '''
        '''
        lines, dLines, dContigs, genomeLen = [], {}, {}, 0
        handle = open(self.filename)
        line = handle.readline()
        contigCnt = 0
        if line[0] == '#' and line[1] == '#':
            self.version = int(line.strip().split()[1])
        for line in handle:
            # No fasta descriptions or comment lines
            if line[0] != '>' and line[0] != '#':
                line = line.strip()
                items = line.split('\t')
                if len(items) > 1: # No fasta nucleotides
                    if items[1] == 'maker': # Approve maker predictions only
                        try:
                            dLines[line]
                        except KeyError:
                            lines.append(line) 
                            dLines[line] = True
                    if items[2] == "contig":
                        try:
                            dContigs[line]
                        except KeyError:
                            genomeLen += int(items[4])
                            dContigs[line] = True
                            contigCnt += 1
        handle.close()
        self.lines = lines
        self.genomeSize = genomeLen
        print "Contig count is %d" %contigCnt


    def rmGenes(self, geneIds):
        '''
        '''
        idxs = []
        cnt = 0
        for line in self.lines:
            items = line.split('\t')
            items[8] = items[8].replace(';', ':')
            geneId = '_'.join(items[8].split(':')[0].split('=')[1].split(self.postfix))[:-1]
            if geneId in geneIds:
                idxs.append(cnt)
            cnt += 1
                    
        idxs = sorted(idxs, reverse=True)
        for idx in idxs:
            del self.lines[idx]


    def stats(self, geneIds):
        '''
        '''
        cntExon, cntIntron, cntCds, cntRna, cntGene, lenExon, lenIntron, lenCds, lenRna, lenGene = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        inGene = False
        prevStart, prevEnd = None, None
        gIds = set()
        for line in self.lines:
            items = line.split('\t')
            items[8] = items[8].replace(';', ':')
            geneId = items[8].split(':')[0].split('=')[1]
            if geneIds == None or geneId in geneIds:
                start, end = int(items[3]), int(items[4])
                length = end - start + 1
                if length < 0: print "Negative Exon"
                if items[2] == "exon":
                    if prevStart == None:
                        lenExon += length
                        cntExon += 1
                    if prevStart != None and prevStart != start and prevEnd != end and geneId.split('-')[-1] == '1':
                        lenExon += length
                        cntExon += 1
                        cntIntron += 1
                        if start > prevEnd:
                            lenBetween = start - prevEnd - 1
                            lenIntron += lenBetween
                            if start - prevEnd - 1 < 0:
                                print "GeneIdA: %s" %geneId
                                print start, end, prevStart, prevEnd
                        else:
                            lenBetween = prevStart - end - 1
                            if prevStart - end - 1 < 0: lenBetween = 0
                            lenIntron += lenBetween
                            if prevStart - end - 1 < 0:
                                pass
                    prevStart, prevEnd = start, end
                if items[2] == "mRNA":
                    lenRna += length
                    cntRna += 1
                    inGene = True
                    prevStart, prevEnd = None, None
                    gId = '_'.join(geneId.split(self.postfix))[:-1]
                    if gId not in gIds:
                        gIds.add(gId)
                        lenGene += length
                        cntGene += 1
                if items[2] == "CDS":
                    inGene = False
                    if geneId.split('-')[-1] == '1':
                        lenCds += length
                        cntCds += 1
                
        print lenExon, cntExon
        print lenIntron, cntIntron
        print lenRna, cntRna
        print lenGene, cntGene
        print lenCds, cntCds
        return (lenExon, cntExon), (lenIntron, cntIntron), (lenRna, cntRna), (lenGene, cntGene), (lenCds, cntCds)
