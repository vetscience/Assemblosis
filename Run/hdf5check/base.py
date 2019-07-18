#!/usr/bin/env python

'''
Oct 10, 2017: Pasi Korhonen, The University of Melbourne

Simplifies system calls, logs and pipe interaction.

'''
import sys, os, time #, ConfigParser
import shlex, subprocess, errno
from threading import Timer

###############################################################################
class Base:
    '''
    '''
    ###########################################################################
    def __init__(self, logHandle = subprocess.PIPE):
        '''
        '''
        self.fname = None
        self.handle = None
        self.log = logHandle


    ###########################################################################
    def ropen(self, fname):
        ''' Allow one to read data either from pipe or file
        '''
        self.handle = None
        self.fname = fname
        if fname == '-':
            self.handle = sys.stdin.readlines()
        else:
            self.handle = open(fname, 'r')
        return self.handle


    ###########################################################################
    def rclose(self):
        ''' Allows one to close the file if reading from pipe is allowed
        '''
        if self.fname != '-': self.handle.close()


    ###########################################################################
    def createDir(self, mydir):
        '''Creates a directory for the assembly if one does not exist yet.
        '''
        try:
            os.makedirs(mydir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    ###########################################################################
    def isNumber(self, myStr):
        '''
        '''
        retVal = True
        try:
            float(myStr)
        except ValueError:
            retVal = False
        return retVal


    ###########################################################################
    def logTime(self, myStr = ""):
        '''
        '''
        if myStr != "": myStr = myStr + ':'
        rt = time.localtime()
        self.log.write("\n------------------------------------------------------------\n")
        self.log.write("%s %d,%d,%d %d:%d:%d\n" %(myStr, rt.tm_year, rt.tm_mon, rt.tm_mday, rt.tm_hour, rt.tm_min, rt.tm_sec))
        self.log.write("------------------------------------------------------------\n\n")


    ###########################################################################
    def setLogHandle(self, handle):
        ''' Log handle should be always set because a full buffer can cease processing
        '''
        self.log = handle


    ###########################################################################
    def closeLogHandle(self):
        ''' Log handle should be always set because a full buffer can cease processing
        '''
        self.log.close()


    ###########################################################################
    def logger(self, myStr):
        ''' Writes a message to the log file
        '''
        self.log.write("## %s\n" %myStr)


    ###########################################################################
    def shell(self, myStr, doPrint = True, myStdout = False, ignoreFailure = False, log = True):
        '''Runs given command in a shell and waits for the command to finish.
        '''
        if log == True:
            self.log.write("# %s\n" %myStr)
        if doPrint == True:
            print ("# %s" %myStr) # is printed as comment line which is easy to remove
        if myStdout == True:
            p = subprocess.Popen(myStr, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        else:
            p = subprocess.Popen(myStr, stdout=self.log, stderr=subprocess.STDOUT, shell=True)
        retVal = p.wait()
        if retVal != 0 and ignoreFailure == False:
            if log == True:
                self.logger("# FAILED (%d): %s" %(retVal, myStr))
            print ("# FAILED (%d): %s" %(retVal, myStr))
            sys.exit(retVal)
        return p


    ###########################################################################
    def _killProc(self, proc, timeout):
        '''
        '''
        timeout["value"] = True
        proc.kill()


    ###########################################################################
    def run(self, cmd, timeoutSec = None, doPrint = True, myStdout = True, ignoreFailure = False, log = True):
        ''' Runs given command in a subprocess and wait for the command to finish.
            Retries 3 times if timeout is given.
        '''
        retryCnt = 0
        while retryCnt < 3:
            if log == True:
                self.log.write("# %s\n" %cmd)
            if doPrint == True:
                print ("# %s" %cdm) # is printed as comment line which is easy to remove
            if myStdout == True:
                proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                proc = subprocess.Popen(shlex.split(cmd), stdout=self.log, stderr=subprocess.PIPE)
            if timeoutSec != None:
                timeout = {"value": False}
                timer = Timer(timeoutSec, self._killProc, [proc, timeout])
                timer.start()
            stdout, stderr = proc.communicate()
            if timeoutSec != None:
                timer.cancel()
            if (proc.returncode > 1 or proc.returncode < 0) and ignoreFailure == False:
                retryCnt += 1
                if retryCnt >= 3: # Tries three times
                    self.logger("## FAILED(%d): %s. Three failures. Exiting ..." %(proc.returncode, cmd))
                    print ("## FAILED(%d): %s. Three failures. Exiting ..." %(proc.returncode, cmd))
                    sys.exit(proc.returncode)
                if log == True:
                    self.logger("## FAILED(%d): %s. Retrying ..." %(proc.returncode, cmd))
                print ("## FAILED(%d): %s. Retrying ..." %(proc.returncode, cmd))
                time.sleep(120) # Wait 2 minutes before the next try
            else:
                break
        return proc

    '''
    ###########################################################################
    def readSection(self, config, section, sep=None):
        #''Reads a section from config parser and returns it a list of item rows
        #''
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
            print("# WARNING: Base::readSection: section '%s' not found ..." %section)
        return mylist
    '''
