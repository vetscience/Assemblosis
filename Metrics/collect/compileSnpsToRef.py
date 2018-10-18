#!/usr/bin/env python

import os, sys, optparse, gzip
from fasta import Fasta

#################################################
def options():
    parser = optparse.OptionParser('usage: python %prog -i filename -n size')
    parser.add_option('-i', '--fasta', dest='fasta', help='FASTA reference', metavar='FASTA', default='')
    parser.add_option('-n', '--snps', dest='snps', help='Nucleotide differences', metavar='SNPS', default='')
    options, args = parser.parse_args()
    return options


#################################################
def main():
    '''
    '''
    opts = options()
    dScafs = {}
    fasta = Fasta(opts.fasta)
    for i in xrange(len(fasta.headers)):
        header = fasta.headers[i].split()[0]
        dScafs[header] = [nt.upper() for nt in fasta.seqs[i]]

    cnt = 0
    with gzip.open(opts.snps) as handle:
        for line in handle:
            items = line.strip().split('\t')
            scafId, pos = items[0], int(items[2])
            scafId = '_'.join(scafId.split("_")[:2])
            indel = False
            if items[3] == "." or items[4] == ".":
                indel = True
            if indel == False:
                fromNt, toNt = items[3].upper(), items[4].upper()
                if dScafs[scafId][pos - 1].upper() == fromNt:
                    dScafs[scafId][pos - 1] = toNt
                    cnt += 1
                else:
                    print >> sys.stderr, "Does not match!!! %s vs %s" %(fromNt, dScafs[scafId][pos - 1])
                    dScafs[scafId][pos - 1] = toNt
                    cnt += 1
    for key in dScafs:
        print ">%s\n%s" %(key, ''.join(dScafs[key]))
    print >> sys.stderr, "SNP count: %d" %cnt


#################################################
if __name__ == "__main__":
    main()
