#! /usr/bin/env python

import os, sys, optparse
import csv, itertools
import re

from fasta import Fasta
from gff import Gff

#################################################
def options():
    parser = optparse.OptionParser('usage: python %prog -s scaffoldsFile -g genesFile')
    parser.add_option('-s', '--scaffolds', dest='scafs', help='Genome scaffolds in fasta format (nt)', metavar='SCAFFOLDS', default='')
    parser.add_option('-g', '--genes', dest='genes', help='Genome genes in fasta format (nt)', metavar='GENES', default='')
    parser.add_option('-r', '--refgen', dest='refGen', help='Reference genome FASTA file', metavar='REFGENOME', default='')
    parser.add_option('-c', '--contamination', dest='contamination', help='File containing identifiers of contaminated genes', metavar='CONTAMINATION', default='')
    options, args = parser.parse_args()
    if options.scafs == '' and options.genes == '' and options.gff == '':
        print '\nPlease, give at least one of genome, gene or gff files:'
        parser.print_help()
        sys.exit(1)
    return options


#################################################
def genomeStats(gff, geneIds):
    '''
    '''
    # First remove redundancy from the collected gff file
    (lenExon, cntExon), (lenIntron, cntIntron), (lenRna, cntRna), (lenGene, cntGene), (lenCds, cntCds) = gff.stats(geneIds)
    print "\n##############################"
    print "Genomic statistics\n"
    print "\tNumber of genes:\t%d (mean length %.2f)" %(cntGene, float(lenGene) / float(cntGene))
    print "\tNumber of mRNAs:\t%d (mean length %.2f)" %(cntRna, float(lenRna) / float(cntRna))
    print "\tNumber of exons:\t%d (mean length %.2f)" %(cntExon, float(lenExon) / float(cntExon))
    print "\tNumber of CDSs:\t%d (mean length %.2f)" %(cntCds, float(lenCds) / float(cntCds))
    print "\tNumber of introns:\t%d (mean length %.2f)" %(cntIntron, float(lenIntron) / float(cntIntron))

    print "\tAverage exon per gene:\t\t%.2f" %(float(cntExon) / float(cntGene))
    print "\tAverage coding domain length per gene:\t%.2f" %(float(lenCds) / float(cntGene))

    print "\tExons altogether:\t%d" %lenExon
    print "\tIntrons altogether:\t%d" %lenIntron

    print "\tGenome size:\t%d" %gff.genomeSize

    print "\tGenomic proportion of exons:\t\t%.2f%%" %(float(lenExon) / float(gff.genomeSize) * 100.0)
    print "\tGenomic proportion of exons and introns\t%.2f%%\n" %(float(lenExon + lenIntron) / float(gff.genomeSize) * 100.0)


#################################################
def detailsFasta(title, fasta, refSize = 0, refSeqCnt = 0):
    '''
    '''

    print "##############################"
    print "%s\n" %title

    # Number of genes
    seqCntTotal = len(fasta.headers)
    print "\tNumber of sequences:\t%d" %seqCntTotal

    # GC content
    shortest, longest = None, 0
    totCnt, nCnt = 0, 0
    aCnt, tCnt, gCnt, cCnt = 0, 0, 0, 0
    gapCnt, noGapSeqsCnt = 0, 0
    for i in xrange(len(fasta.seqs)):
        seq = fasta.seqs[i]
        myLen = len(seq)
        seq = seq.upper()
        nCnt += seq.count('N')
        aCnt += seq.count('A')
        tCnt += seq.count('T')
        gCnt += seq.count('G')
        cCnt += seq.count('C')
        totCnt += myLen
        if myLen > longest: longest = myLen
        if shortest == None: shortest = myLen
        if myLen < shortest: shortest = myLen
        # Find gap count in the fasta sequence
        newGapCnt = len(re.findall("[N]+", seq))
        if newGapCnt == 0:
            noGapSeqsCnt += 1
        gapCnt += newGapCnt

    ntCnt = aCnt + tCnt + gCnt + cCnt
    print "\t%.2f%%:\t%d\tout of %d nucleotides are Ns" %(float(nCnt) / float(totCnt) * 100.0, nCnt, totCnt)
    print "\t%.2f%%:\t%d\tout of %d nucleotides are As" %(float(aCnt) / float(totCnt) * 100.0, aCnt, totCnt)
    print "\t%.2f%%:\t%d\tout of %d nucleotides are Ts" %(float(tCnt) / float(totCnt) * 100.0, tCnt, totCnt)
    print "\t%.2f%%:\t%d\tout of %d nucleotides are Cs" %(float(cCnt) / float(totCnt) * 100.0, cCnt, totCnt)
    print "\t%.2f%%:\t%d\tout of %d nucleotides are Gs" %(float(gCnt) / float(totCnt) * 100.0, gCnt, totCnt)
    print "\tCG content is %.2f%% %d out of %d are GCs" %(float(cCnt + gCnt) / float(ntCnt) * 100.0, cCnt + gCnt, ntCnt)
    print "\tNumber of gaps is %d" %gapCnt
    print "\tNumber of sequences without gaps is %d\n" %noGapSeqsCnt

    # Print N10, N20, N30, N40, N50, N60, N70, N80, N90 values
    nValCnt = 0
    fasta.seqs.sort(key = len)
    myPrint10, myPrint20, myPrint30 = True, True, True
    myPrint40, myPrint50, myPrint60 = True, True, True
    myPrint70, myPrint80, myPrint90 = True, True, True
    seqCnt = 1
    for seq in fasta.seqs:
        nValCnt += len(seq)
        if nValCnt >= totCnt * (10 - 1) / 10 and myPrint10 == True:
            print "\tN10: %d\tSeqCnt > N10: %d" %(len(seq), seqCntTotal - seqCnt + 1)
            myPrint10 = False
        if nValCnt >= totCnt * (10 - 2) / 10 and myPrint20 == True:
            print "\tN20: %d\tSeqCnt > N20: %d" %(len(seq), seqCntTotal - seqCnt + 1)
            myPrint20 = False
        if nValCnt >= totCnt * (10 - 3) / 10 and myPrint30 == True:
            print "\tN30: %d\tSeqCnt > N30: %d" %(len(seq), seqCntTotal - seqCnt + 1)
            myPrint30 = False
        if nValCnt >= totCnt * (10 - 4) / 10 and myPrint40 == True:
            print "\tN40: %d\tSeqCnt > N40: %d" %(len(seq), seqCntTotal - seqCnt + 1)
            myPrint40 = False
        if nValCnt >= totCnt * (10 - 5) / 10 and myPrint50 == True:
            print "\tN50: %d\tSeqCnt > N50: %d" %(len(seq), seqCntTotal - seqCnt + 1)
            myPrint50 = False
        if nValCnt >= totCnt * (10 - 6) / 10 and myPrint60 == True:
            print "\tN60: %d\tSeqCnt > N60: %d" %(len(seq), seqCntTotal - seqCnt + 1)
            myPrint60 = False
        if nValCnt >= totCnt * (10 - 7) / 10 and myPrint70 == True:
            print "\tN70: %d\tSeqCnt > N70: %d" %(len(seq), seqCntTotal - seqCnt + 1)
            myPrint70 = False
        if nValCnt >= totCnt * (10 - 8) / 10 and myPrint80 == True:
            print "\tN80: %d\tSeqCnt > N80: %d" %(len(seq), seqCntTotal - seqCnt + 1)
            myPrint80 = False
        if nValCnt >= totCnt * (10 - 9) / 10 and myPrint90 == True:
            print "\tN90: %d\tSeqCnt > N90: %d" %(len(seq), seqCntTotal - seqCnt + 1)
            myPrint90 = False
        seqCnt += 1
    if refSize > 0:
        print ""
        nValCnt = 0
        myPrint10, myPrint20, myPrint30 = True, True, True
        myPrint40, myPrint50, myPrint60 = True, True, True
        myPrint70, myPrint80, myPrint90 = True, True, True
        seqCnt = 1
        for seq in fasta.seqs:
            nValCnt += len(seq)
            if nValCnt >= refSize * (10 - 1) / 10 and myPrint10 == True:
                print "\tNG10: %d\tSeqCnt > NG10: %d" %(len(seq), seqCntTotal - seqCnt + 1)
                myPrint10 = False
            if nValCnt >= refSize * (10 - 2) / 10 and myPrint20 == True:
                print "\tNG20: %d\tSeqCnt > NG20: %d" %(len(seq), seqCntTotal - seqCnt + 1)
                myPrint20 = False
            if nValCnt >= refSize * (10 - 3) / 10 and myPrint30 == True:
                print "\tNG30: %d\tSeqCnt > NG30: %d" %(len(seq), seqCntTotal - seqCnt + 1)
                myPrint30 = False
            if nValCnt >= refSize * (10 - 4) / 10 and myPrint40 == True:
                print "\tNG40: %d\tSeqCnt > NG40: %d" %(len(seq), seqCntTotal - seqCnt + 1)
                myPrint40 = False
            if nValCnt >= refSize * (10 - 5) / 10 and myPrint50 == True:
                print "\tNG50: %d\tSeqCnt > NG50: %d" %(len(seq), seqCntTotal - seqCnt + 1)
                myPrint50 = False
            if nValCnt >= refSize * (10 - 6) / 10 and myPrint60 == True:
                print "\tNG60: %d\tSeqCnt > NG60: %d" %(len(seq), seqCntTotal - seqCnt + 1)
                myPrint60 = False
            if nValCnt >= refSize * (10 - 7) / 10 and myPrint70 == True:
                print "\tNG70: %d\tSeqCnt > NG70: %d" %(len(seq), seqCntTotal - seqCnt + 1)
                myPrint70 = False
            if nValCnt >= refSize * (10 - 8) / 10 and myPrint80 == True:
                print "\tNG80: %d\tSeqCnt > NG80: %d" %(len(seq), seqCntTotal - seqCnt + 1)
                myPrint80 = False
            if nValCnt >= refSize * (10 - 9) / 10 and myPrint90 == True:
                print "\tNG90: %d\tSeqCnt > NG90: %d" %(len(seq), seqCntTotal - seqCnt + 1)
                myPrint90 = False
            seqCnt += 1
    print "\n\tLength of the genome:\t%d" %totCnt
    print "\tLongest sequence:\t%d" %longest
    print "\tShortest sequence:\t%d" %shortest
    print "\tAverage length:\t%.2f" %(float(totCnt) / float(seqCntTotal))
    print "\n"
    return totCnt

    
    


#################################################
def main():
    '''
    '''
    opts = options()
    refSize, refSeqCnt = 0, 0
    try:
        ref = Fasta(opts.refGen)
        refSize, refSeqCnt = ref.totalLen, len(ref.headers)
    except IOError:
        pass
        
    geneIds = set()
    if opts.contamination != "":
        handle = open(opts.contamination, 'r')
        for line in handle:
            myId = line.strip().split('\t')[0]
            if myId[0] != '#':
                geneIds.add(myId)
        handle.close()
    geneIds = list(geneIds)
    myGeneIds = None

    genomeSize = None
    if opts.scafs != '':
        fastaS = Fasta(opts.scafs)
        genomeSize = detailsFasta("Genome Scaffolds", fastaS, refSize, refSeqCnt)
    if opts.genes != '':
        fastaG = Fasta(opts.genes)
        fastaG.rmGenes(geneIds)
        myGeneIds = set([header.split()[0] for header in fastaG.headers])
        detailsFasta("Genome genes", fastaG)


#################################################
if __name__ == "__main__":
    main()
