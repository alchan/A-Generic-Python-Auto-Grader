###############################################################
# Auto-Grader (See "A Generic Python Auto-Grader")            #
# File: Utilities.py                                          #
# Author: Albert Chan                                         #
# Affiliation: Fayetteville State University                  #
#              Department of Mathematics and Computer Science #
# Copyright (c) 2019                                          #
# License: GPL 2.0                                            #
# Exception: Tester.pyc and the generated TestData.pyc can be #
#            distributed to students without source or        #
#            showing the license                              #
###############################################################

import re

# It is not common, but some language does allow nested comments - and we are prepared for it
# Some langauges allow multiple comment styles, so we use a list
# (start_comment_marker, end_comment_marker, nested_comment_allowed)
pythonComments = [('#', '\n', False)]
haskellComments = [('--', '\n', False), ('{-', '-}', True)]
javaComments = [('//', '\n', False), ('/*', '*/', False)] # also for C/C++

CR = chr (13) # MacOS newline
LF = chr (10) # Linux newline
CRLF = CR+LF  # Windows newline

def normalize1 (program):
    """ Convert to Linux style newline characters """
    return program.replace (CRLF, LF).replace (CR, LF)

def wc (program):
    """ Count number of characters, words, and lines in program """
    return len (program), len (program.split ()), len (program.split (LF))

def skipComments (program, start, end, nested, index):
    """ Skip the comments in code, leaving only the comment mark """
    # we found the start_comment_marker at index, we need to skip to the end_comment_marker
    # and return where the comment ends
    n = len (program)
    ns = len (start)
    ne = len (end)
    i = index + ns
    while i < n:
        if program [i] == '\\':    # Escape character, so next character should be treated as normal character
            # skip next character
            i = i + 2
            continue
        if program [i:i+ne] == end: # Found the end comment marker
            return i + ne
        if nested:
            if program [i:i+ns] == start: # Found a nested comment
                i = skipComments (program, start, end, nested, i)
                continue
        i = i + 1
    return n # pattern not found, return index for end-of-file

def skipString (program, quote, index):
    # we found the start of a string at index, skip to the end of the string and return where it ends
    n = len (program)
    k = len (quote)
    i = index + k
    while i < n:
        if program [i] == '\\':   # do not process escaped character
            # skip next character
            i = i + 2
            continue
        if program [i:i+k] == quote:  # found the end quote
            return i + k
        i = i + 1
    return n # pattern not found, return index for end-of-file

def normalize2 (program, comments = pythonComments):
    # this function assume program is a valid program and will do the followings:
    # 1. replace all comments with a comment marker
    # 2. replace all strings and/or doc-strings with ''
    # 3. replace all out-of-string escape character with a single backslash
    n = len (program)
    result = []
    i = 0
    while i < n:
        commentEncountered = False
        for start, end, nested in comments:    # handle comments
            m = len (start)
            if program [i:i+m] == start:
                result.append (start + end)
                i = skipComments (program, start, end, nested, i)
                commentEncountered = True
                break
        if commentEncountered:
            continue
        if program [i] == '\\':      # handle escaped character, should never happen here
            # skip next charcter
            result.append (program [i])
            i = i + 2
            continue
        if program [i:i+3] == '"""':     # handle docstring
            # skipp docString
            result.append ("''")
            i = skipString (program, '"""', i)
            continue
        if program [i:i+3] == "'''":      # handle docstring
            # skipp docString
            result.append ("''")
            i = skipString (program, "'''", i)
            continue
        if program [i] == '"':           # handle string
            # skip string
            result.append ("''")
            i = skipString (program, '"', i)
            continue
        if program [i] == "'":            # handle string
            # skip string
            result.append ("''")
            i = skipString (program, "'", i)
            continue
        result.append (program [i])      # not in comment or string, so it is part of the program
        i = i + 1
    return ''.join (result).split (LF)   # convert the list back to a string

def countFeature (program, keyword, useRE = True):
    """ Count the number of features in a program """
    if useRE:
        return len ([line for line in program if re.search (r"\b" + keyword + r"\b", line)])
    else:
        return len ([line for line in program if keyword in line])

def countBlankLines (program):
    """ Count the number of blank lines """
    return len ([line for line in program if not line.strip ()])

def getStats (program):
    """ Collect statistics about the program """
    program = normalize1 (program)
    nChars, nWords, nLines = wc (program)
    program = normalize2 (program)
    nBlankLines = countBlankLines (program)
    nComments = countFeature (program, '#', False)
    nImports = countFeature (program, 'import')
    nGlobals = countFeature (program, 'global')
    nClasses = countFeature (program, 'class')
    nFunctions = countFeature (program, 'def')
    nTopLevelFunctions = len ([line for line in program if line.startswith ('def ')])
    nTopLevelClasses = len ([line for line in program if line.startswith ('class ')])
    return (nChars, nWords, nLines, nBlankLines, nComments, nImports, nGlobals, nClasses, nFunctions, nTopLevelClasses, nTopLevelFunctions)

def formatProgram (program):
    return "*****\n* " + "\n* ".join (program.split ('\n')) + "\n*****"

def getYesNoInput (prompt):
    try:
        answer = raw_input (prompt + ' ')
    except:
        answer = input (prompt)
    return answer.lower ().startswith ('y')
