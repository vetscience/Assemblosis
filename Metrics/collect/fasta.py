#!/usr/bin/env python

import sys
from base import Base

class Fasta(Base):
    '''
    '''
    
    def __init__(self, filename = None, shortheader = False, lineCnt = None):
        '''shortheader cuts the header to first separator
        '''
        self.myfile = filename
        self.headers = []
        self.seqs = []
        self.idxs = None
        self.totalLen = 0
        if filename != None:
            self._read(lineCnt)
            if shortheader == True:
               self._cutheader()
            self._check()
            self.idxs = [i for i in xrange(len(self.headers))]


    def rmGenes(self, geneIds):
        '''
        '''
        headers = []
        for header in self.headers:
            item = header.split()[0]
            headers.append(item)
        for item in geneIds:
            try:
                idx = headers.index(item)
                del self.headers[idx]
                del self.seqs[idx]
            except ValueError:
                print >> sys.stderr, "Fasta::rmGenes: could not delete item %s" %item


    def header(self, i):
        '''
        '''
        return self.headers[self.idxs[i]]


    def seq(self, i):
        '''
        '''
        return self.seqs[self.idxs[i]]


    def filter(self, headers):
        '''
        '''
        newseqs = []
        commons = list(set(self.headers) & set(headers))
        for item in commons:
            idx = self.headers.index(item)
            newseqs.append(self.seqs[idx])
        self.headers = commons
        self.seqs = newseqs
        self._check()


    def myprint(self):
        '''
        '''
        for i in xrange(len(self.headers)):
            print '>' + self.headers[self.idxs[i]] + '\n',
            print self.seqs[self.idxs[i]] + '\n',


    def split(self, file1, file2):
        '''Split the file in two (every second row)
        '''
        h1, h2, s1, s2 = [], [], [], []
        for i in xrange(len(self.headers)):
            if i % 2 == 0:
                h1.append(self.headers[self.idxs[i]])
                s1.append(self.seqs[self.idxs[i]])
            else:
                h2.append(self.headers[self.idxs[i]])
                s2.append(self.seqs[self.idxs[i]])
        self.write(file1, None, h1, s1)
        self.write(file2, None, h2, s2)


    def write(self, filename = None, cnt = None, headers = None, seqs = None):
        '''
        '''
        if filename == None: filename = self.myfile
        if headers == None: headers = self.headers
        if seqs == None: seqs = self.seqs
        handle = open(filename, 'w')
        for i in xrange(len(headers)):
            if cnt != None:
                if i >= cnt: break
            handle.write('>' + headers[self.idxs[i]] + '\n')
            handle.write(seqs[self.idxs[i]] + '\n')
        handle.close()


    def _read(self, lineCnt):
        '''
        '''
        handle = self.ropen(self.myfile)
        myseq = ""
        found = False
        cnt = 0
        for line in handle:
            line = line.strip()
            if len(line) > 0:
                if line[0] == '>':
                    if found == True:
                        self.seqs.append(myseq)
                        self.totalLen += len(myseq)
                    self.headers.append(line[1::])
                    myseq = ""
                    found = True
                else:
                    myseq += line
                cnt += 1
                if lineCnt != None and cnt >= lineCnt: break
        if found == True:
            self.seqs.append(myseq)
            self.totalLen += len(myseq)
        self.rclose()


    def _cutheader(self):
        '''
        '''
        headers = []
        for item in self.headers:
            newheader = item.split()[0]
            headers.append(newheader)
        self.headers = headers


    def _check(self):
        '''
        '''
        if len(self.headers) != len(self.seqs):
            print "Fasta::__init__: number of the headers does not match to the number of the sequences %d vs. %d" %(len(self.headers), len(self.seqs))
        
    def getDict(self):
        '''
        '''
        myd = {}
        for i in xrange(len(self.headers)): myd[self.headers[i]] = self.seqs[i]
        return myd


