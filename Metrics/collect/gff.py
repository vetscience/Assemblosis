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
                        #print line,
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
            #Hco_2011.12.k21_007170  maker   gene    3648    3867    .       -       .       ID=maker-Hco_2011%2E12%2Ek21_007170-augustus-gene-0.1;Name=maker-Hco_2011%252E12%252Ek21_007170-augustus-gene-0.1;
            items[8] = items[8].replace(';', ':')
            #geneId = items[8].split(':')[0].split('=')[1].split(self.postfix)[0]
            geneId = '_'.join(items[8].split(':')[0].split('=')[1].split(self.postfix))[:-1]
            if geneId in geneIds:
                idxs.append(cnt)
                #try:
                #    idx = self.lines.index(geneId)
                #    idxs.add(idx)
                #except ValueError:
                #    print >> sys.stderr, "Fasta::rmGenes: could not delete item %s" %geneId
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
                #if prevStart != None:
                #    if start == prevStart:
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
                                #sys.exit(0)
                        else:
                            lenBetween = prevStart - end - 1
                            if prevStart - end - 1 < 0: lenBetween = 0
                            lenIntron += lenBetween
                            if prevStart - end - 1 < 0:
                                pass
                                #print "GeneIdB: %s" %geneId
                                #print start, end, prevStart, prevEnd
                                #sys.exit(0)
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
                #if items[2] == "gene":
                #    lenGene += length
                #    cntGene += 1
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
                
 
'''
##gff-version 3
Hco_2011.12.k21_115497  .       contig  1       305     .       .       .       ID=Hco_2011.12.k21_115497;Name=Hco_2011.12.k21_115497;
##FASTA
>Hco_2011.12.k21_115497
GAAAAAAGCGATATACCAAGTTTTAAGGATGAACATTTTATTAACGGCATATAAACAGTT
TGCCATCGCTTGTATAGGCGATCTGTAAGTTATAGAACTCTCGGAATCTTCACAAACTCG
TGACAGTTAAGGGTGGAGAATTTGTCATTTATTATATCAATTCCTGGGCATAACTAAAGT
ATAAACTGATCAGAATACAGATAAATTCTTAATAAAATCATCATGCTAAAGTGTTTCTGA
TGTGGATACCATACTTCAAATCCATATATTCAAAATTCAACACATATCCTTGTCCCAATC
CAACA
##gff-version 3
Hco_2011.12.k21_007170  .       contig  1       4504    .       .       .       ID=Hco_2011.12.k21_007170;Name=Hco_2011.12.k21_007170;
Hco_2011.12.k21_007170  maker   gene    3648    3867    .       -       .       ID=maker-Hco_2011%2E12%2Ek21_007170-augustus-gene-0.1;Name=maker-Hco_2011%252E12%252Ek21_007170-augustus-gene-0.1;
Hco_2011.12.k21_007170  maker   mRNA    3648    3867    .       -       .       ID=maker-Hco_2011%2E12%2Ek21_007170-augustus-gene-0.1-mRNA-1;Parent=maker-Hco_2011%2E12%2Ek21_007170-augustus-gene-0.1;Name=maker-Hco_2011%252E12%252Ek21_007170-augustus-gene-0.1-mRNA-1;_AED=0.23;_eAED=0.23;_QI=51|1|0|1|1|0|2|0|30;
Hco_2011.12.k21_007170  maker   exon    3648    3746    0.71    -       .       ID=maker-Hco_2011%2E12%2Ek21_007170-augustus-gene-0.1-mRNA-1:exon:4911;Parent=maker-Hco_2011%2E12%2Ek21_007170-augustus-gene-0.1-mRNA-1;
Hco_2011.12.k21_007170  maker   exon    3826    3867    0.71    -       .       ID=maker-Hco_2011%2E12%2Ek21_007170-augustus-gene-0.1-mRNA-1:exon:4912;Parent=maker-Hco_2011%2E12%2Ek21_007170-augustus-gene-0.1-mRNA-1;
Hco_2011.12.k21_007170  maker   CDS     3648    3737    .       -       0       ID=maker-Hco_2011%2E12%2Ek21_007170-augustus-gene-0.1-mRNA-1:cds:5209;Parent=maker-Hco_2011%2E12%2Ek21_007170-augustus-gene-0.1-mRNA-1;
Hco_2011.12.k21_007170  est_gff:tophat  expressed_sequence_match        3712    3866    1       -       .
       ID=Hco_2011.12.k21_007170:hit:56829;Name=2:JUNC00175088;score=1;
Hco_2011.12.k21_007170  est_gff:tophat  match_part      3826    3866    1       -       .       ID=Hco_2011.12.k21_007170:hsp:156013;Parent=Hco_2011.12.k21_007170:hit:56829;Name=2:JUNC00175088;Target=2:JUNC00175088 36 190 +;Gap=M41;
Hco_2011.12.k21_007170  est_gff:tophat  match_part      3712    3746    1       -       .       ID=Hco_2011.12.k21_007170:hsp:156014;Parent=Hco_2011.12.k21_007170:hit:56829;Name=2:JUNC00175088;Target=2:JUNC00175088 1 35 +;Gap=M35;
Hco_2011.12.k21_007170  snap_masked     match   3507    3869    39.558  -       .       ID=Hco_2011.12.k21_007170:hit:56830;Name=snap_masked-Hco_2011%252E12%252Ek21_007170-abinit-gene-0.0-mRNA-1;_AED=0.29;_eAED=0.29;
Hco_2011.12.k21_007170  snap_masked     match_part      3826    3869    12.020  -       .       ID=Hco_2011.12.k21_007170:hsp:156015;Parent=Hco_2011.12.k21_007170:hit:56830;Name=snap_masked-Hco_2011%25252E12%25252Ek21_007170-abinit-gene-0.0-mRNA-1;Target=snap_masked-Hco_2011%25252E12%25252Ek21_007170-abinit-gene-0.0-mRNA-1 140 183 +;Gap=M44;
Hco_2011.12.k21_007170  snap_masked     match_part      3628    3746    12.341  -       .       ID=Hco_2011.12.k21_007170:hsp:156016;Parent=Hco_2011.12.k21_007170:hit:56830;Name=snap_masked-Hco_2011%25252E12%25252Ek21_007170-abinit-gene-0.0-mRNA-1;Target=snap_masked-Hco_2011%25252E12%25252Ek21_007170-abinit-gene-0.0-mRNA-1 21 139 +;Gap=M119;
Hco_2011.12.k21_007170  snap_masked     match_part      3507    3526    15.197  -       .       ID=Hco_2011.12.k21_007170:hsp:156017;Parent=Hco_2011.12.k21_007170:hit:56830;Name=snap_masked-Hco_2011%25252E12%25252Ek21_007170-abinit-gene-0.0-mRNA-1;Target=snap_masked-Hco_2011%25252E12%25252Ek21_007170-abinit-gene-0.0-mRNA-1 1 20 +;Gap=M20;
##FASTA
>Hco_2011.12.k21_007170
'''
