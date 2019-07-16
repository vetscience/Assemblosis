#!/usr/bin/env python

'''
Oct 26, 2017: Pasi Korhonen, The University of Melbourne

Create a file for H5 files, or if they don't exist, FASTQ


'''

import os, sys, random, argparse, multiprocessing
from multiprocessing import Process
from os import walk

#################################################
def args():
    parser = argparse.ArgumentParser('python %prog ')
    parser.add_argument('-d', '--dir', dest='data', help='Directory, in which PacBio data resides', metavar='DATADIR', default='Data')
    #parser.add_argument('-q', '--fastq', dest='fastq', help='PacBio reads are subreads in FASTQ format instead of HDF5.', metavar='FASTQ', default='false')
    parser.add_argument('-f', '--fofn', dest='fofn', help='Filename for fofn containing the names for all found bax files.', metavar='FOFN', default='allBaxFiles.fofn')
    return parser.parse_args()


#################################################
class Fofn:
    '''
    '''
    #################################################
    def __init__(self, dataDir):
        '''
        '''
        self.wd = dataDir


    #################################################
    def checkFileExistence(self, files):
        '''
        '''
        for item in files:
            if os.path.exists(item) == False:
                print "# FATAL ERROR: file %s, given in configuration file, does not exist. Exiting..." %item
                sys.exit(-1)


    #################################################
    def pbReads(self): #, fastq):
        '''
        '''
        reads = set()
        for (dirpath, dirnames, filenames) in walk(self.wd, followlinks = True):
            #print dirpath, dirnames, filenames
            for filename in filenames:
                #if fastq == "false":
                    if "bax.h5" in filename[-6:]:
                        reads.add("%s/%s" %(os.path.abspath(dirpath), filename))
                #else:
                #    if "fastq.gz" in filename[-8:]:
                #        reads.add("%s/%s" %(os.path.abspath(dirpath), filename))
        return sorted(reads)


    #################################################
    def createFofn(self, resFile, reads):
        '''
        '''
        if len(reads) == 0:
            print >> sys.stderr, "# FATAL ERROR: cannot find PacBio reads. Exiting ..."
            sys.exit(-1)
        with open("%s" %resFile, 'w') as handle:
            for read in reads:
                handle.write("%s\n" %read)


#################################################
def main():
    '''
    '''
    opts = args()

    fofn = Fofn(opts.data)
    # Write all identified bax files to a file of file names (fofn)
    reads = fofn.pbReads() #opts.fastq)
    fofn.createFofn(opts.fofn, reads)


#################################################
if __name__ == "__main__":
    main()
