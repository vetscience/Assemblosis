#!/usr/bin/env python

import os, sys, optparse
from fasta import Fasta

#################################################
def options():
    parser = optparse.OptionParser('usage: python %prog -i filename -n size')
    parser.add_option('-1', '--fasta1', dest='fasta1', help='FASTA1 reference', metavar='FASTA1', default='')
    parser.add_option('-2', '--fasta2', dest='fasta2', help='FASTA2 reference', metavar='FASTA2', default='')
    options, args = parser.parse_args()
    return options


#################################################
def main():
    '''
    '''
    opts = options()
    dScafs1 = {}
    fasta1 = Fasta(opts.fasta1)
    for i in xrange(len(fasta1.headers)):
        header = fasta1.headers[i].split()[0]
        dScafs1[header] = fasta1.seqs[i].upper()
    cnt = 0
    ids = set()
    fasta2 = Fasta(opts.fasta2)
    for i in xrange(len(fasta2.headers)):
        header = fasta2.headers[i].split()[0]
        fasta2.seqs[i] = fasta2.seqs[i].upper()
        tmpCnt = 0
        for j in xrange(min(len(fasta2.seqs[i]), len(dScafs1[header]))):
            if fasta2.seqs[i][j] != dScafs1[header][j]:
                cnt += 1 
                tmpCnt += 1
                ids.add(header)
        lenDiff = abs(len(fasta2.seqs[i]) - len(dScafs1[header]))
        cnt += lenDiff
    print cnt
    print >> sys.stderr, '\t'.join(sorted(ids))


#################################################
if __name__ == "__main__":
    main()
