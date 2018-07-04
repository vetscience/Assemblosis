#!/usr/bin/env python

import os, sys, optparse
from wbtree import WbTree

#################################################
def options():
    parser = optparse.OptionParser('usage: python %prog -i filename -n size')
    parser.add_option('-i', '--gff', dest='gff', help='GFF file to filter', metavar='GFF', default='-')
    #parser.add_option('-n', '--size', dest='size', help='Minimum accepted sequence size (default=30)', metavar='SIZE', default='30')
    #parser.add_option('-r', '--order', dest='order', action='store_true', help='Longest first (default=FALSE)', default=False)
    #parser.add_option('-a', '--assemble', dest='assemble', action='store_true', help='Do assembly', default=False)
    options, args = parser.parse_args()
    if options.gff == '':
        parser.print_help()
        sys.exit(1)
    return options


#################################################
def main():
    '''
    '''
    opts = options()
    tree = WbTree()
    tree.parse(opts.gff, False)
    tree.rmVars()
    print tree


#################################################
if __name__ == "__main__":
    main()
