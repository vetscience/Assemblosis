#!/usr/bin/env python

import os, sys, subprocess, random
import argparse, ConfigParser
from multiprocessing import Process
from base import Base
from fasta import Fasta
from os import listdir, walk
from os.path import isfile, join

#################################################
def args():
    '''
    '''
    parser = argparse.ArgumentParser('usage: python %prog [options] -g ref.fa')
    parser.add_argument('-i', '--assembly', dest='assembly', help='Genomic assembly in FASTA format', metavar='ASSEMBLY', default='')
    parser.add_argument('-m', '--masked', dest='assemblyMasked', help='Soft-masked genomic assembly in FASTA format', metavar='MASKED', default='')
    parser.add_argument('-r', '--reads', dest='trimmedReads', help='Trimmed reads', metavar='TRIMMEDREADS', default='')
    #parser.add_argument('-d', '--dir', dest='wd', help='Working directory', metavar='DIR', default='workDir')
    parser.add_argument('-T', '--threads', dest='pCnt', help='Number of parallel threads (default 24)', metavar='THREADS', default='24')
   
    arguments = parser.parse_args()
    if arguments.assembly == '':
        print '\nScaffolds file has to be given:'
        parser.print_help()
        #print arguments
        sys.exit(1)
    return arguments

#################################################
class HaploMerger(Base):
    '''
    '''
    #################################################
    def __init__(self, workDir, pCnt):
        '''
        '''
        Base.__init__(self)
        self.wd = workDir
        self.smrtHome = None
        self.createDir(workDir)
        self.pCnt = int(pCnt)
        self.logHandle = None


    #################################################
    def setSmrtPath(self, smrtHome):
        '''
        '''
        self.smrtHome = smrtHome


    #################################################
    def renameFasta(self, iName, oName, mName, prefix = "scaf"):
        '''
        '''
        fasta = Fasta(iName)
        with open(mName, 'w') as handleM: # Mapping
            with open(oName, 'w') as handleW: # Output
                cnt = 1
                for i in xrange(len(fasta.headers)):
                    newHeader = "%s%ds" %(prefix, cnt)
                    handleW.write(">%s\n" %newHeader)
                    handleW.write("%s\n" %fasta.seqs[i])
                    handleM.write("%s\t%s\n" %(newHeader, fasta.headers[i])) 
                    cnt += 1


    #################################################
    def checkFileExistence(self, files):
        '''
        '''
        for item in files:
            if os.path.exists(item) == False:
                print "FATAL: file %s, given in configuration file, does not exist. Exiting..." %item
                sys.exit(-1)


    #################################################
    def deleteReads(self):
        '''
        '''
        self.shell("rm -f %s/reads.f*" %self.wd)


    #################################################
    def haploMerger(self, refName, refNameMasked, trimmedReads, identity = 90):
        '''
        '''
        fasta = Fasta("%s/%s" %(self.wd, refName))
        self.shell("rm -rf %s/HaploRun" %self.wd)
        self.createDir("%s/HaploRun" %self.wd)
        self.shell("touch %s/HaploRun/scoreMatrix.q" %self.wd)
        if len(fasta.headers) <= 1:
          self.shell("cp %s/%s %s/%s.haplomerged.fa" %(self.wd, refName, self.wd, '.'.join(refName.split('.')[:-1])))
          return refName
        self.shell("cp -r $HAPLOMERGER_DIR/project_template/* %s/HaploRun/" %self.wd)
        self.shell("cp -r $HAPLOMERGER_DIR/bin %s/" %self.wd)
        scoreMatrix = self._inferScoreMatrix(refNameMasked, "%s" %trimmedReads, identity)
        #scoreMatrix = self._inferScoreMatrix("%s" %refNameMasked, identity)
        self.shell("mv %s/scoreMatrix.q %s/HaploRun/" %(self.wd, self.wd)) # Overwrite the default matrix
        self.shell("cp %s/%s %s/HaploRun/" %(self.wd, scoreMatrix, self.wd)) # Overwrite the default matrix
        self.renameFasta("%s/%s" %(self.wd, refNameMasked), "%s/HaploRun/masked.fa" %self.wd, "%s/HaploRun/masked.mapping" %self.wd)
        self.shell("gzip -f %s/HaploRun/masked.fa" %self.wd)
        fasta = Fasta("%s/%s" %(self.wd, refNameMasked))
        tgtSize = int(fasta.totalLen / self.pCnt) + 1
        memDir = os.getcwd()
        seqName = "masked"
        os.chdir("%s/HaploRun" %self.wd)
        self.shell("sed 's/threads=1/threads=%d/1;s/targetSize=50000000/targetSize=%d/1;s/querySize=1600000000/querySize=%d/1' $HAPLOMERGER_DIR/project_template/hm.batchA1.initiation_and_all_lastz > hm.batchA1.initiation_and_all_lastz" %(self.pCnt, tgtSize, fasta.totalLen + 1))
        self.shell("sed 's/threads=1/threads=%d/1' $HAPLOMERGER_DIR/project_template/hm.batchA2.chainNet_and_netToMaf > hm.batchA2.chainNet_and_netToMaf" %self.pCnt)
        self.shell("sed 's/threads=1/threads=%d/1;s/targetSize=50000000/targetSize=%d/1;s/querySize=1600000000/querySize=%d/1' $HAPLOMERGER_DIR/project_template/hm.batchB1.initiation_and_all_lastz > hm.batchB1.initiation_and_all_lastz" %(self.pCnt, tgtSize, fasta.totalLen + 1))
        self.shell("sed 's/threads=1/threads=%d/1' $HAPLOMERGER_DIR/project_template/hm.batchB2.chainNet_and_netToMaf > hm.batchB2.chainNet_and_netToMaf" %self.pCnt)
        self.shell("sed 's/threads=1/threads=%d/1' $HAPLOMERGER_DIR/project_template/hm.batchB4.refine_unpaired_sequences > hm.batchB4.refine_unpaired_sequences" %self.pCnt)
        self.shell("sed 's/threads=1/threads=%d/1;s/targetSize=50000000/targetSize=%d/1;s/querySize=1600000000/querySize=%d/1' $HAPLOMERGER_DIR/project_template/hm.batchD1.initiation_and_all_lastz > hm.batchD1.initiation_and_all_lastz" %(self.pCnt, tgtSize, fasta.totalLen + 1))
        self.shell("sed 's/threads=1/threads=%d/1' $HAPLOMERGER_DIR/project_template/hm.batchD2.chainNet_and_netToMaf > hm.batchD2.chainNet_and_netToMaf" %self.pCnt)
        for i in xrange(3): # Run three times to avoid misjoints
            self.shell("./hm.batchA1.initiation_and_all_lastz %s" %seqName)
            self.shell("./hm.batchA2.chainNet_and_netToMaf %s" %seqName)
            self.shell("./hm.batchA3.misjoin_processing %s" %seqName)
            seqName = "%s_A" %seqName
        self.shell("./hm.batchB1.initiation_and_all_lastz %s" %seqName)
        self.shell("./hm.batchB2.chainNet_and_netToMaf %s" %seqName)
        self.shell("./hm.batchB3.haplomerger %s" %seqName)
        self.shell("zcat %s.%sx.result/optiNewScaffolds.fa.gz > test.fa" %(seqName, seqName))
        fasta = Fasta("test.fa")
        if len(fasta.headers) > 0:
            self.shell("./hm.batchB4.refine_unpaired_sequences %s" %seqName)
            self.shell("./hm.batchB5.merge_paired_and_unpaired_sequences %s" %seqName)
            seqName = "%s_ref" %seqName
            filterAli = [4000, 2400, 1000]
            minLen = [5000, 3000, 1500]
            for i in xrange(3):
                self.shell("sed 's/filterAli=2500/filterAli=%d/1;s/minLen=2500/minLen=%d/1' $HAPLOMERGER_DIR/project_template/hm.batchD3.remove_tandem_assemblies > hm.batchD3.remove_tandem_assemblies" %(filterAli[i], minLen[i]))
                self.shell("./hm.batchD1.initiation_and_all_lastz %s" %seqName)
                self.shell("./hm.batchD2.chainNet_and_netToMaf %s" %seqName)
                self.shell("./hm.batchD3.remove_tandem_assemblies %s" %seqName)
                seqName = "%s_D" %seqName
            self.shell("zcat %s.fa.gz > ../%s.haplomerged.fa" %(seqName, '.'.join(refName.split('.')[:-1])))
        else:
            self.shell("zcat %s.%sx.result/unpaired.fa.gz > ../%s.haplomerged.fa" %(seqName, seqName, '.'.join(refName.split('.')[:-1])))
        #self.shell("rm -rf " %(self.wd, self.wd, self.wd, self.wd))
        os.chdir(memDir)
        return "%s.haplomerged.fa" %'.'.join(refName.split('.')[:-1])


    #################################################
    def n50(self, assembly):
        '''
        '''
        fasta = Fasta("%s" %assembly)
        n50, nValCnt = None, 0
        fasta.seqs.sort(key = len)
        for seq in fasta.seqs:
            nValCnt += len(seq)
            if nValCnt >= fasta.totalLen / 2:
                n50 = len(seq)
                break
        return n50


    #################################################
    def merge(self, contigs):
        '''
        '''
        memDir = os.getcwd()
        os.chdir(self.wd)

        rnContigs = []
        for i in xrange(len(contigs)):
            assembly = contigs[i]
            newName = "%s.rn.fa" %'.'.join(assembly.split(".")[:-1])
            mapName = "%s.mapping" %'.'.join(assembly.split(".")[:-1])
            self.renameFasta(assembly, newName, mapName, "scafs%d_" %(i + 1))
            rnContigs.append(newName)
            
        assembly = rnContigs[0]
        self.shell("cp %s tomerge.fasta" %assembly)
        for i in xrange(1, len(rnContigs)):
            assembly = rnContigs[i]
            n50, alnLen  = self.n50("tomerge.fasta"), 5000
            print "N50: ", n50
            self.shell("nucmer -l 100 -prefix out tomerge.fasta %s" %assembly)
            self.shell("delta-filter -i 95 -r -q out.delta > out.rq.delta")
            self.shell("quickmerge -d out.rq.delta -q %s -r tomerge.fasta -hco 5.0 -c 1.5 -l %d -ml %d" %(assembly, n50, alnLen))
            self.shell("cp merged.fasta tomerge.fasta")
        self.shell("cp merged.fasta merged.assembly.fasta")
        os.chdir(memDir)
        return "merged.assembly.fasta"


    #################################################
    def _splitSeqsIn2Files(self, fasta, refName, multiplier = 0.1):
        '''
        '''
        #memDir = os.getcwd()
        #os.chdir(self.wd)
        fName1, fName2 = "%s.1.fa" %refName, "%s.2.fa" %refName
        #fasta = Fasta(refName)
        if len(fasta.headers) == 0:
            print "# FATAL ERROR: FASTA file %s is empty. Exiting ..." %refName
        elif len(fasta.headers) == 1:
            seqlen = len(fasta.seqs[0])
            seq1 = fasta.seqs[0][:int(seqlen * multiplier)]
            seq2 = fasta.seqs[0][int(seqlen * multiplier):]
            with open(fName1, 'w') as handle:
                handle.write(">%s_1\n" %fasta.headers[0])
                handle.write("%s\n" %seq1)
            with open(fName2, 'w') as handle:
                handle.write(">%s_2\n" %fasta.headers[0])
                handle.write("%s\n" %seq2)
            #self.shell("gzip -f %s %s" %(fName1, fName2))
        else:
            fasta.order(reverse = True) # Longest first
            targetLen = int(fasta.totalLen * multiplier)
            #deltaLen = int(fasta.totalLen * 0.05)
            deltaLen = int(fasta.totalLen * 0.01)
            seqLen = 0
            found = False
            with open(fName1, 'w') as handle1:
                with open(fName2, 'w') as handle2:
                    for i in xrange(len(fasta.headers)):
                        if found == False:
                            handle1.write(">%s_1\n" %fasta.header(i))
                            handle1.write("%s\n" %fasta.seq(i))
                            seqLen += len(fasta.seq(i))
                            if seqLen <= targetLen + deltaLen and seqLen >= targetLen - deltaLen or seqLen > targetLen + deltaLen:
                                found = True
                        if found == True:
                            handle2.write(">%s_2\n" %fasta.header(i))
                            handle2.write("%s\n" %fasta.seq(i))
            if found == False or seqLen > targetLen + deltaLen:
                print "## WARNING: the procedure to infer the score matrix for haplomerger may not succeed, because"
                print "##          the sequences could not be split according to the instructions: (%d / %d) = %.3f" %(seqLen, fasta.totalLen, float(seqLen) / float(fasta.totalLen))
        #os.chdir(memDir)
        return fName1, fName2

    #################################################
    def median(self, vals):
        '''
        '''
        retVal = None
        cnt = len(vals)
        vals = sorted(vals)
        if cnt < 1:
            return None
        idx = cnt // 2
        if cnt % 2 == 1:
            retVal = vals[idx]
        else:
            retVal  = sum(vals[(idx - 1):(idx + 1)]) / 2.0
        return retVal


    #################################################
    def _median(self):
        '''
        '''
        base = Base()
        scoreFiles = set()
        for (dirpath, dirnames, filenames) in walk(".", followlinks = False):
            #print dirpath, dirnames, filenames
            for filename in filenames:
                if ".q" in filename[-2:] and "subset" in filename[:6]:
                    scoreFiles.add("%s/%s" %(dirpath, filename))
            break
        #print scoreFiles
        matrices = sorted(scoreFiles)
        matrixList = []
        for i in xrange(len(matrices)):
            matrixList.append([])
            with open(matrices[i]) as handle:
                #print "####"
                cnt = 0
                for line in handle:
                    line = line.strip()
                    items = line.split()
                    if cnt >= 16:
                        matrixList[-1].append([int(item) for item in items])
                        #print line
                    cnt += 1
        matrix = []
        newMatrixList = []
        #print matrixList
        for i in xrange(len(matrixList[0])):
            newMatrixList.append([])
            matrix.append([])
            for j in xrange(len(matrixList[0][0])):
                newMatrixList[-1].append([])
                for k in xrange(len(matrixList)):
                    newMatrixList[-1][-1].append(matrixList[k][i][j])
                matrix[-1].append(self.median(newMatrixList[-1][-1]))
        #print matrixList
        #print newMatrixList
        with open("scoreMatrix.q", "w") as handle:
            handle.write("\tA\tC\tG\tT\n")
            for i in xrange(len(matrix)):
                handle.write("\t%s\n" %'\t'.join([str(int(item)) for item in matrix[i]]))
        #print matrix
        

    #################################################
    def _inferScoreMatrix(self, refName, trimmedReads, identity):
        '''
        '''
        memDir = os.getcwd()
        os.chdir(self.wd)
        fraction = 0.1
        fasta = Fasta(trimmedReads)
        iterCnt, seqCnt = 300, 1000
        self.shell("rm -f *.q runs.txt subset*")
        random.seed(0)
        with open("runs.txt", "w") as handle:
            for i in xrange(iterCnt):
                subFasta = Fasta()
                subIdxs = random.sample(xrange(len(fasta.headers)), int(seqCnt))
                subFasta.headers, subFasta.seqs = [fasta.headers[j] for j in subIdxs], [fasta.seqs[k] for k in subIdxs]
                subFasta.totalLen = sum([len(fasta.seqs[j]) for j in subIdxs])
                fName1, fName2 = self._splitSeqsIn2Files(subFasta, "subset%d" %(i + 1), fraction)
                handle.write("lastz_D_Wrapper.pl --target=%s --query=%s --identity=%d\n" %(fName1, fName2, identity))
        self.shell("cat runs.txt | parallel -j %d" %self.pCnt, ignoreFailure = True)
        self._median()
        self.shell("rm -f subset*")
        #self.shell("tail -n 5 *.q > scoreMatrix.q")
        if os.path.exists("scoreMatrix.q") == False:
            print >> sys.stderr, "# FATAL ERROR: could not create score matrix for HaploMerger. Exiting ..."
            sys.exit(0)
        first = refName.split(".")[0]
        scoreMatrix = "%s.%s.q" %(first, first)
        print "cp scoreMatrix.q %s" %scoreMatrix
        self.shell("cp scoreMatrix.q %s" %scoreMatrix)
        os.chdir(memDir)
        return scoreMatrix


    #################################################
    def predictRna(self):
        '''
        '''
        self.shell("cmscan --cpu %d --cut_tc -o %s/infernal.out --tblout %s/infernal.tbl %s/Rfam.cm %s" %(self.pCnt, self.wd, self.wd, self.infernalDb, self.genomeFile))
        self.shell("tRNAscan-SE -o %s/trnase.tbl %s"  %(self.wd, self.genomeFile))


#################################################
#################################################
#################################################
def main():
    '''
    '''
    opts = args()

    wd = "workDir"
    assembler = HaploMerger(wd, opts.pCnt)
    loghandle = open(wd + "/log.txt", "w")
    assembler.setLogHandle(loghandle)

    print >> sys.stderr, "\n####################\n### HaploMerger2\n"
    assembly = opts.assembly.split('/')[-1]
    assemblyMasked = opts.assemblyMasked.split('/')[-1]
    trimmedReads = opts.trimmedReads.split('/')[-1]
    zipped = False
    if ".gz" in trimmedReads[-3:]:
        zipped = True
        trimmedReads = trimmedReads[:-3]
    assembler.shell("cp %s %s/%s" %(opts.assembly, wd, assembly))
    assembler.shell("cp %s %s/%s" %(opts.assemblyMasked, wd, assemblyMasked))
    if zipped == True:
        assembler.shell("zcat %s > %s/%s" %(opts.trimmedReads, wd, trimmedReads))
    else:
        assembler.shell("cp %s %s/%s" %(opts.trimmedReads, wd, trimmedReads))
    contigs = assembler.haploMerger(assembly, assemblyMasked, trimmedReads)
    print "HaploMerger: ", contigs

    assembler.logTime("End")
    loghandle.close()


#################################################
if __name__ == "__main__":
    main()
