###############################################################
# Auto-Grader (See "A Generic Python Auto-Grader")            #
# File: DataGen.py                                            #
# Author: Albert Chan                                         #
# Affiliation: Fayetteville State University                  #
#              Department of Mathematics and Computer Science #
# Copyright (c) 2019                                          #
# License: GPL 2.0                                            #
# Exception: Tester.pyc and the generated TestData.pyc can be #
#            distributed to students without source or        #
#            showing the license                              #
###############################################################

from ModelSolution import function, getRandomInput, nTestCases, dataFileName

def generateOneTestCase (tcID, function, getRandomInput):
    """ Generate one testcase """
    result = None
    exception = None
    inData = getRandomInput ()
    try:
        result = function (inData)
    except Exception as err:
        exception = type (err).__name__
    return (tcID, inData, result, exception)

def generateTestSuite (n, funtion, getRandomInput):
    """ Generate a test suite """
    return [generateOneTestCase (i, funtion, getRandomInput) for i in range (1, n + 1)]

def testCase2String (testcase):
    """ Convert testcase to string """
    return '(%s, %s, %s, %s)' % tuple (repr (x) for x in testcase)

def testSuite2String (testSuite):
    """ Convert test suite to string """
    return "tests = [" + ",\n         ".join ([testCase2String (testcase) for testcase in testSuite]) + "]\n"

def generateTestDataFile (filename, n, funtion, getRandomInput):
    """ Generate a test suite and write to data file """
    testSuite = generateTestSuite (n, function, getRandomInput)
    f = open (filename, 'w')
    writeHeader (f)
    f.write (testSuite2String (testSuite))
    f.close ()

def writeHeader (fileHandle):
    fileHandle.write ('###############################################################\n')
    fileHandle.write ('# Auto Grader (See "A Generic Python Auto Grader")            #\n')
    fileHandle.write ('# File: TestData.py                                           #\n')
    fileHandle.write ('# Author: Albert Chan                                         #\n')
    fileHandle.write ('# Affiliation: Fayetteville State University                  #\n')
    fileHandle.write ('#              Department of Mathematics and Computer Science #\n')
    fileHandle.write ('# Copyright (c) 2019                                          #\n')
    fileHandle.write ('# License: GPL 2.0                                            #\n')
    fileHandle.write ('# Exception: Tester.pyc and the generated TestData.pyc can be #\n')
    fileHandle.write ('#            distributed to students without source or        #\n')
    fileHandle.write ('#            showing the license                              #\n')
    fileHandle.write ('###############################################################\n')
    fileHandle.write ('\n')

generateTestDataFile (dataFileName+'.py', nTestCases, function, getRandomInput)
