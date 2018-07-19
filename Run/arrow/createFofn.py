#!/usr/bin/env python

'''
Oct 26, 2017: Pasi Korhonen, The University of Melbourne

Uses dextract to convert all hdf5 files in given directory (and subdirectories) into
given result directory


'''

import os, sys, random, argparse, multiprocessing
from multiprocessing import Process
from os import walk

#################################################
def args():
    parser = argparse.ArgumentParser('python %prog ')
    parser.add_argument('-d', '--dir', dest='data', help='Directory, in which PacBio data resides', metavar='DATADIR', default='Data')
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
    def pbReads(self):
        '''
        '''
        readsH5 = set()
        for (dirpath, dirnames, filenames) in walk(self.wd, followlinks = True):
            #print dirpath, dirnames, filenames
            for filename in filenames:
                if "bax.h5" in filename[-6:]:
                    readsH5.add("%s/%s" %(os.path.abspath(dirpath), filename))
        return sorted(readsH5)


    #################################################
    def createFofn(self, resFile, readsH5):
        '''
        '''
        if len(readsH5) == 0:
            print >> sys.stderr, "# FATAL ERROR: cannot find PacBio reads. Exiting ..."
            sys.exit(-1)
        with open("%s" %resFile, 'w') as handle:
            for read in readsH5:
                handle.write("%s\n" %read)


#################################################
def main():
    '''
    '''
    opts = args()

    fofn = Fofn(opts.data)
    # Write all identified bax files to a file of file names (fofn)
    readsH5 = fofn.pbReads()
    fofn.createFofn(opts.fofn, readsH5)


#################################################
if __name__ == "__main__":
    main()
