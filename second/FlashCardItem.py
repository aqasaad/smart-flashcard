#! /usr/bin/env python
#
# Author: Jack Hebert (jhebert@gmail.com)
#
# A signle Flashcard - it has a history of the times
# that it has been asked, how to display itself,
# the question it poses, the answer, and which learning
# sets that it belongs to.

import time

class FlashCardItem:
  def __init__(self):
    self.questionText = None
    self.answerText = None
    self.history = None
    self.lastAskTime = 0

  def PrintQuestion(self):
    self.lastAskTime = time.time()
    print self.questionText

  def IsCorrectAnswer(self, answer):
    return False



