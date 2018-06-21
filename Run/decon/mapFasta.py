#!/usr/bin/env python

import os, sys, optparse, random
from base import Base
from fasta import Fasta

#################################################
def options():
    parser = optparse.OptionParser('usage: python %prog -i filename -n size')
    parser.add_option('-i', '--fasta', dest='fasta', help='FASTA contig file', metavar='FASTA', default='-')
    parser.add_option('-s', '--select', dest='select', help='Identiers in this file are used to select the sequences', metavar='SELECT', default='-')
    parser.add_option('-m', '--map', dest='map', help='Identifier mappings file', metavar='MAPPINGS', default='')
    parser.add_option('-r', '--reverse', dest='reverse', action='store_true', help='Do reverse mapping', default=False)
    #parser.add_option('-p', '--percentage', dest='percentage', help='The percentage of reads to sample', metavar='PERCENTAGE', default='')
    options, args = parser.parse_args()
    if options.fasta == '' or options.map == '':
        parser.print_help()
        sys.exit(1)
    return options

#################################################
def main():
    '''
    '''
    opts = options()
    dMap = {}
    handle = open(opts.map, 'r')
    for line in handle:
        items = line.strip().split('\t')
        if opts.reverse == True:
            dMap[items[0]] = items[1]
        else:
            dMap[items[1]] = items[0]
    handle.close()

    dIds = {}
    handle = open(opts.select, 'r')
    for line in handle:
        dIds[line.strip()] = True
    handle.close()

    base = Base()
    handle = base.ropen(opts.fasta)
    found = True
    for line in handle:
        line = line.strip()
        if line[0] == ">":
            try:
                dIds[line[1:]]
                found = True
            except KeyError:
                found = False
                continue
            try:
                line = ">%s" %dMap[line[1:]]
            except KeyError:
                print >> sys.stderr, "## WARNING: key %s not found ..." %line[1:]
        if found == True:
            print "%s" %line
    base.rclose()


#################################################
if __name__ == "__main__":
    main()
