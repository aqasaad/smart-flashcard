#! /usr/bin/env python
#
# Author: Jack Hebert (jhebert@gmail.com)
#
# Managers the sessions that have previously been gone
# through so as to estimate the current state of knowledge.
#
# TODO (jhebert): Wrap these methods in try and except
# blocks and return appropriate empty values in failure.


import pickle

class SessionHistory:
  def __init__(self):
    pass

  def SaveSession(self, questionSequence, fileName):
    binaryString = pickle.dumps(questionSequence)
    f = open(fileName, 'w')
    f.write(binaryString)

  def LoadSession(self, fileName):
    binaryString = open(fileName).read()
    questionSequence = pickle.loads(binaryString)
    return questionSequence
