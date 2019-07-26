#!/usr/bin/env python

'''
Oct 26, 2017: Pasi Korhonen, The University of Melbourne

Uses dextract to convert all hdf5 files in given directory (and subdirectories) into
given result directory


'''

import os, sys, random, argparse, multiprocessing
from multiprocessing import Process
from os import walk
import base

#################################################
def args():
    parser = argparse.ArgumentParser('python %prog ')
    parser.add_argument('-d', '--dir', dest='data', help='Directory, in which PacBio data resides', metavar='DATADIR', default='Data')
    parser.add_argument('-r', '--res', dest='res', help='Result directory', metavar='RESDIR', default='Results')
    parser.add_argument('-T', '--threads', dest='pCnt', help='Number of parallel threads (default is half of the capacity but >= 1)', metavar='THREADS', default='0')
    parser.add_argument('-b', '--bam', dest='bam', help='Search for BAM files instead of h5 files', action='store_true', default=False)
    return parser.parse_args()


#################################################
class Dextractor(base.Base):
    '''
    '''
    #################################################
    def __init__(self, dataDir, resDir, pCnt):
        '''
        '''
        base.Base.__init__(self)
        self.wd = dataDir
        self.shell("rm -rf %s" %resDir, log = False)
        self.createDir(resDir)
        self.pCnt = int(pCnt)
        self.setLogHandle(open("%s/log.txt" %resDir, "w"))


    #################################################
    def checkFileExistence(self, files):
        '''
        '''
        for item in files:
            if os.path.exists(item) == False:
                print ("# FATAL ERROR: file %s, given in configuration file, does not exist. Exiting..." %item)
                sys.exit(-1)


    #################################################
    def pbReads(self):
        '''
        '''
        readsH5, readsFa, readsFq = set(), set(), set()
        for (dirpath, dirnames, filenames) in walk(self.wd, followlinks = True):
            #print dirpath, dirnames, filenames
            for filename in filenames:
                if "bax.h5" in filename[-6:]:
                    readsH5.add("%s/%s" %(dirpath, filename))
                if ".fasta" in filename[-6:]:
                    readsFa.add("%s/%s" %(dirpath, filename))
                if ".fastq" in filename[-6:]:
                    readsFq.add("%s/%s" %(dirpath, filename))
        return sorted(readsH5), sorted(readsFa), sorted(readsFq)


    #################################################
    def createFastaAndFastqReads(self, resDir, readsH5, readsFa, readsFq):
        '''
        '''
        if len(readsH5) == 0:
            print ("# FATAL ERROR: cannot find PacBio reads. Exiting ...")
            sys.exit(-1)
        #if (len(readsFa) != len(readsH5) or len(readsFq) != len(readsH5)) and len(readsH5) > 0:
        with open("%s/runs.sh" %resDir, 'w') as handle:
            for read in readsH5:
                resRead = read.split("/")[-1]
                #handle.write("dextract %s > %s/%s.fasta\n" %(read, resDir, resRead))
                handle.write("dextract -q %s > %s/%s.fastq\n" %(read, resDir, resRead))
                #self.logger("dextract %s > %s/%s.fasta" %(read, resDir, resRead))
                self.logger("dextract -q %s > %s/%s.fastq" %(read, resDir, resRead))
        self.shell("parallel -j %d < %s/runs.sh" %(self.pCnt, resDir))
        self.shell("cat %s/*.fastq > %s/pbReads.fastq" %(resDir, resDir))
        #self.shell("cat %s/*.fasta > %s/pbReads.fasta" %(resDir, resDir))
        for read in readsH5:
            resRead = read.split("/")[-1]
            #self.shell("rm %s/%s.fasta" %(resDir, resRead))
            self.shell("rm %s/%s.fastq" %(resDir, resRead))


#################################################
class Bam(base.Base):
    '''
    '''
    #################################################
    def __init__(self, dataDir, resDir, pCnt):
        '''
        '''
        base.Base.__init__(self)
        self.wd = dataDir
        self.shell("rm -rf %s" %resDir, log = False)
        self.createDir(resDir)
        self.pCnt = int(pCnt)
        self.setLogHandle(open("%s/log.txt" %resDir, "w"))


    #################################################
    def checkFileExistence(self, files):
        '''
        '''
        for item in files:
            if os.path.exists(item) == False:
                print ("# FATAL ERROR: file %s, given in configuration file, does not exist. Exiting..." %item)
                sys.exit(-1)


    #################################################
    def pbReads(self):
        '''
        '''
        readsBam = set()
        for (dirpath, dirnames, filenames) in walk(self.wd, followlinks = True):
            #print dirpath, dirnames, filenames
            for filename in filenames:
                if ".bam" in filename[-4:]:
                    readsBam.add("%s/%s" %(dirpath, filename))
        return sorted(readsBam)


    #################################################
    def createBamReads(self, resDir, readsBam):
        '''
        '''
        if len(readsBam) == 0:
            print ("# FATAL ERROR: cannot find PacBio read fastq files. Exiting ...")
            sys.exit(-1)
        with open("%s/runs.sh" %resDir, 'w') as handle:
            for read in readsBam:
                resRead = read.split("/")[-1]
                handle.write("/home/miniconda3/bin/bedtools bamtofastq -i %s -fq %s/%s.fastq\n" %(read, resDir, resRead))
        self.shell("parallel -j %d < %s/runs.sh" %(self.pCnt, resDir))
        self.shell("cat %s/*.fastq > %s/pbReads.fastq" %(resDir, resDir))
        for read in readsBam:
            resRead = read.split("/")[-1]
            self.shell("rm %s/%s.fastq" %(resDir, resRead))


#################################################
def main():
    '''
    '''
    opts = args()

    pCnt = int(opts.pCnt)
    if pCnt == 0:
        pCnt = int(float(multiprocessing.cpu_count()) / 2.0 + 0.5)

    if opts.bam == True:
        bam = Bam(opts.data, opts.res, pCnt)
        bam.logTime("Start")
        readsBam = bam.pbReads()
        bam.createBamReads(opts.res, readsBam)
        bam.logTime("End")
        bam.closeLogHandle()
    else:
        dextractor = Dextractor(opts.data, opts.res, pCnt)
        dextractor.logTime("Start")
        # Convert hdf5 reads to FASTA and FASTQ formats into the given result directory
        readsH5, readsFa, readsFq = dextractor.pbReads()
        dextractor.createFastaAndFastqReads(opts.res, readsH5, readsFa, readsFq)
        dextractor.logTime("End")
        dextractor.closeLogHandle()


#################################################
if __name__ == "__main__":
    main()
