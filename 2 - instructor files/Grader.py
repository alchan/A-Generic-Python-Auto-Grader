###############################################################
# Auto-Grader (See "A Generic Python Auto-Grader")            #
# File: Grader.py                                             #
# Author: Albert Chan                                         #
# Affiliation: Fayetteville State University                  #
#              Department of Mathematics and Computer Science #
# Copyright (c) 2019                                          #
# License: GPL 2.0                                            #
# Exception: Tester.pyc and the generated TestData.pyc can be #
#            distributed to students without source or        #
#            showing the license                              #
###############################################################

from os import sep
from Tester import loadFunction, runAllTests
from Utilities import getStats
from zipfile import ZipFile

testData = 'TestData'
path = 'submissions.zip'
maxScore = 100

def openfile (filename, mode = 'r'):
    """ Open a file, should work in both Pyton 2 and 3 """
    try:
        return file (filename, mode)
    except NameError:
        return open (filename, mode)

def readfile (zip, filename):
    """ Read data from a file inside a zip file """
    f = zip.open (filename)
    content = f.read ()
    f.close ()
    return content.decode ('utf-8')

def getRecordingFunction (log = None):
    """ Return a function that will log to a file as well as output to screen """
    def record (message = None):
        if message is None:
            message = ''
        if log:
            log.write ('%s\n' % message)
        print (message)
    return record

def extractStudentLoginAndFileName (filename):
    """ extract the student login and student submmitted filename from the filename download from Canvas submission """
    components = filename.split ('_')
    return components [0], components [-1]

def removeExtension (filename):
    """ Remove extension from a file """
    return filename [:filename.rfind ('.')]

def gradeOneStudent (testSuite, filename, path, zip, log):
    """ Grade one student """
    student, fname = extractStudentLoginAndFileName (filename)
    record = getRecordingFunction (log)
    record ('**********')
    record ('Processing file [%s] submitted by %s' % (fname, student))
    record ('**********')

    module = removeExtension (filename)
    print (module)
    score = runAllTests (testSuite, module, path, record)
    record ('**********')
    record ('Execution score: %.2f of %.2f' % (score, maxScore))
    record ('**********')

    stats = getStats (readfile (zip, filename))
    # do whatever you want with the stats
    # note that since score from the grader is returned
    # you can updated and display it based on the stats, if you like

    # Example:
    factor = 1.0
    if not stats [5] == 0: # imports
        factor = factor - 0.5
        record ('Usage of import detected, you score will be deducted by 50%% or %.2f' % (score * 0.5))
    if not stats [10] == 1: # top level functions
        factor = factor - 0.2
        record ('Defined more than one function, your score will be deducted by 20%% or %.2f' % (score * 0.2))
    score = score * factor
    record ('**********')
    record ('Final score: %.2f of %.2f' % (score, maxScore))
    record ('**********')

    record ('**********')
    record ('Finished processing')
    record ('**********')
    record ()

def gradeAllStudents ():
    """ Grade all students """
    zip = ZipFile (path)
    log = openfile ('grades.txt', 'w')
    tests = loadFunction (testData, '.', 'tests')
    for filename in sorted (zip.namelist ()):
        if filename.endswith ('.py'):
            gradeOneStudent (tests, filename, path, zip, log)
    log.close ()

gradeAllStudents ()
