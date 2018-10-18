#!/usr/bin/env python

import os, sys, optparse
from Utils import Fasta

#################################################
def options():
    parser = optparse.OptionParser('usage: python %prog -i filename -n size')
    parser.add_option('-i', '--fasta', dest='fasta', help='FASTA file to filter', metavar='FASTA', default='-')
    parser.add_option('-r', '--order', dest='order', action='store_true', help='Longest first (default=FALSE)', default=False)
    options, args = parser.parse_args()
    if options.fasta == '':
        parser.print_help()
        sys.exit(1)
    return options


#################################################
def main():
    '''
    '''
    opts = options()
    fasta = Fasta(opts.fasta)
    if opts.order == True:
        print >> sys.stderr, "# Ordering ..."
        fasta.order(True)
    cnt, totalCnt = 0, 0
    for i in xrange(len(fasta.headers)):
        print ">%s" %fasta.header(i)
        for c in fasta.seqs[i]:
            if c in ['a','c','g','t']: cnt += 1
            totalCnt += 1
        print "%s" %fasta.seq(i).upper()
    print >> sys.stderr, "# %d / %d = %.3f %%" %(cnt, totalCnt, float(cnt) / float(totalCnt) * 100.0)

#################################################
if __name__ == "__main__":
    main()
