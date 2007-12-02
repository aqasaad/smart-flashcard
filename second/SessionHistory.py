#! /usr/bin/env python
#
# Author: Jack Hebert (jhebert@gmail.com)
#
# Managers the sessions that have previously been gone
# through so as to estimate the current state of knowledge.
#


import pickle

class SessionHistory:
  def __init__(self):
    pass

  def SaveSession(self, flashcards, fileName):
    questionSequence = flashcards.history
    print 'Saving:', questionSequence
    binaryString = pickle.dumps(questionSequence)
    success = False
    try:
      f = open(fileName, 'w')
      f.write(binaryString)
      f.close()
      success = True
    except IOError:
      print 'Error opening file to write:', fileName
    return success

  def LoadSession(self, fileName):
    questionSequence = None
    try:
      binaryString = open(fileName).read()
      questionSequence = pickle.loads(binaryString)
      print 'Loading:', questionSequence
    except IOError:
      print 'Error opening session history file:', fileName
    return questionSequence

