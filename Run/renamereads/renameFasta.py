#!/usr/bin/env python

import os, sys, optparse
from base import Base

#################################################
def options():
    parser = optparse.OptionParser('usage: "python %prog -i filename -f reffile" or "cat file | python %prog -i - -f reffile" or "cat file | python %prog -f reffile"')
    parser.add_option('-i', '--fasta', dest='fasta', help='FASTA file to filter', metavar='FASTA', default='-')
    parser.add_option('-p', '--prefix', dest='prefix', help='Prefix in renamed FASTA header', metavar='PREFIX', default='Seq')
    parser.add_option('-m', '--mapped', dest='mapped', help='Mapped identifiers', metavar='MAPPED', default='mapped.ids')
    #parser.add_option('-a', '--assemble', dest='assemble', action='store_true', help='Do assembly', default=False)
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
    prefix = opts.prefix
    #fasta = Fasta(opts.fasta)
    base = Base()
    handle = base.ropen(opts.fasta)

    cnt = 1
    with open(opts.mapped, "w") as handleW:
        for line in handle:
            if line[0] == ">":
                newHeader = "%s%ds" %(prefix, cnt)
                print ">%s" %newHeader
                handleW.write("%s\t%s\n" %(newHeader, line.strip()[1:]) )
                cnt += 1
            else:
                print line,
    base.rclose()


#################################################
if __name__ == "__main__":
    main()
