#!/usr/bin/env python

'''
Allows transparent stdin usage via pipe into the program when optparser is used.
Input parameters are e.g. "-i -" in which "-" defines the usage of stdin.
E.g:
parser = optparse.OptionParser('usage: python %prog')
parser.add_option('-i', '--ifile', dest='ifile', help='Name of the file', default='-')
options, args = parser.parse_args()
handle = self.ropen(options.ifile)
for line in handle:
    items = line.strip().split()
self.rclose()

Usage above:
cat file.txt | python myprog.py -i - | less
or 
cat file.txt | python myprog.py | less

'''
import sys, os, time, ConfigParser
import shlex, subprocess, errno
from threading import Timer

class Base:
    '''
    '''
    def __init__(self, loghandle = subprocess.PIPE):
        '''
        '''
        self.fname = None
        self.handle = None
        self.log = loghandle


    def ropen(self, fname):
        '''
        '''
        self.handle = None
        self.fname = fname
        if fname == '-':
            self.handle = sys.stdin.readlines()
        else:
            self.handle = open(fname, 'r')
        return self.handle


    def rclose(self):
        '''
        '''
        if self.fname != '-': self.handle.close()


    def createDir(self, mydir):
        '''Creates a directory for the assembly if one does not exist yet.
        '''
        try:
            os.makedirs(mydir)
            #print "\nCreated directory %s" %mydir
        except OSError, e:
            #print "\nDirectory %s was already existing" %mydir
            if e.errno != errno.EEXIST:
                raise

    def isNumber(self, myStr):
        '''
        '''
        retVal = True
        try:
            float(myStr)
        except ValueError:
            retVal = False
        return retVal


    def logTime(self, mystr = ""):
        '''
        '''
        if mystr != "": mystr = mystr + ':'
        rt = time.localtime()
        self.log.write("\n------------------------------------------------------------\n")
        self.log.write("%s %d,%d,%d %d:%d:%d\n" %(mystr, rt.tm_year, rt.tm_mon, rt.tm_mday, rt.tm_hour, rt.tm_min, rt.tm_sec))
        self.log.write("------------------------------------------------------------\n\n")


    def setHandle(self, handle = subprocess.PIPE):
        '''
        '''
        self.log = handle


    def shell(self, mystr, doprint = True, mystdout = False, ignoreFailure = False):
        '''Runs the given shell command in a subprocess and wait for it to finish.
        '''
        if doprint == True:
            print >> sys.stderr, "# " + mystr # is printed as comment line which is easy to remove
        if mystdout == True:
            p = subprocess.Popen(mystr, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        else:
            p = subprocess.Popen(mystr, stdout=self.log, stderr=subprocess.STDOUT, shell=True)
            #p = subprocess.Popen(mystr, stdout=self.log, stderr=subprocess.PIPE, shell=True)
        retVal = p.wait()
        if retVal != 0 and ignoreFailure == False:
            print "FAILED (%d): %s" %(retVal, mystr)
            sys.exit(retVal)
        return p


    def _kill_proc(self, proc, timeout):
        '''
        '''
        timeout["value"] = True
        proc.kill()

    def run(self, cmd, timeout_sec = None, doprint = True, mystdout = True, ignoreFailure = False):
        '''
        '''
        retryCnt = 0
        while retryCnt < 3:
            if doprint == True:
                print >> sys.stderr, "# " + cmd # is printed as comment line which is easy to remove
            if mystdout == True:
                proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                #proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                proc = subprocess.Popen(shlex.split(cmd), stdout=self.log, stderr=subprocess.PIPE)
                #proc = subprocess.Popen(cmd, stdout=self.log, stderr=subprocess.PIPE)
            if timeout_sec != None:
                timeout = {"value": False}
                timer = Timer(timeout_sec, self._kill_proc, [proc, timeout])
                timer.start()
            stdout, stderr = proc.communicate()
            if timeout_sec != None:
                timer.cancel()
            if (proc.returncode > 1 or proc.returncode < 0) and ignoreFailure == False:
                retryCnt += 1
                if retryCnt >= 3: # Tries three times
                    print >> sys.stderr, "## FAILED(%d): %s. Three failures. Exiting ..." %(proc.returncode, cmd)
                    sys.exit(proc.returncode)
                print >> sys.stderr, "## FAILED(%d): %s. Retrying ..." %(proc.returncode, cmd)
                time.sleep(120) # Wait 2 minutes before the next try
            else:
                break
        return proc
            #return proc.returncode, stdout.decode("utf-8"), stderr.decode("utf-8"), timeout["value"]


    def readSection(self, config, section, sep=None):
        '''Reads a section from config parser and returns it a list of item rows
        '''
        mylist = []
        try:
            lines = config.options(section)
            lines = sorted(lines)
            for line in lines:
                items = config.get(section, line).split()
                if sep != None: items = config.get(section, line).split(sep)
                try:
                    if items[0][0] != '#': # Comment line
                        mylist.append(items)
                except IndexError:
                    pass
        except ConfigParser.NoSectionError:
            print "Base::readSection: section '%s' not found. Exiting..." %section
            sys.exit(1)
        return mylist
    
