#!/usr/bin/env python

import os, sys, optparse, gzip
from fasta import Fasta

#################################################
def options():
    parser = optparse.OptionParser('usage: python %prog -i filename -n size')
    parser.add_option('-i', '--fasta', dest='fasta', help='FASTA reference', metavar='FASTA', default='')
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
    fasta = Fasta(opts.fasta)
    for i in xrange(len(fasta.headers)):
        header = fasta.headers[i].split()[0]
        dScafs[header] = [nt.upper() for nt in fasta.seqs[i]]

    cnt = 0
    with gzip.open(opts.snps) as handle:
        for line in handle:
            items = line.strip().split('\t')
            scafId, pos = items[0], int(items[2])
            scafId = '_'.join(scafId.split("_")[:-2])
            indel = False
            if items[3] == "." or items[4] == ".":
                indel = True
            if indel == False:
                fromNt, toNt = items[3].upper(), items[4].upper()
                try:
                  if dScafs[scafId][pos - 1].upper() == fromNt:
                    dScafs[scafId][pos - 1] = toNt
                    cnt += 1
                  else:
                    print >> sys.stderr, "Does not match!!! %s vs %s" %(fromNt, dScafs[scafId][pos - 1])
                    dScafs[scafId][pos - 1] = toNt
                    cnt += 1
                except KeyError:
                  pass
    for key in dScafs:
        print ">%s\n%s" %(key, ''.join(dScafs[key]))
    print >> sys.stderr, "SNP count: %d" %cnt
    #print "%d SNPs and %d indels in %d CDSs in %d mRNAs, %d outside CDSs of which %d are indels and rest %d SNPs" %(cnt - indelCnt, indelCnt, sum([dCdsCnt[key] for key in dCdsCnt]), sum([dMrnaCnt[key] for key in dMrnaCnt]), totalCnt - cnt, totalIndelCnt - indelCnt, totalCnt - cnt - totalIndelCnt + indelCnt)


#################################################
if __name__ == "__main__":
    main()
