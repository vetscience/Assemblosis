#!/usr/bin/env python

import os, sys, optparse, random
from fasta import Fasta

#################################################
def options():
    parser = optparse.OptionParser('usage: python %prog -i filename -n size')
    parser.add_option('-i', '--fasta', dest='fasta', help='FASTA contig file', metavar='FASTA', default='-')
    #parser.add_option('-p', '--percentage', dest='percentage', help='The percentage of reads to sample', metavar='PERCENTAGE', default='')
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
    for i in xrange(len(fasta.headers)):
        print ">%s" %fasta.header(i)
        print fasta.seq(i)
    

#################################################
if __name__ == "__main__":
    main()
