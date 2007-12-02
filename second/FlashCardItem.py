#! /usr/bin/env python
#
# Author: Jack Hebert (jhebert@gmail.com)
#
# A signle Flashcard - it has a history of the times
# that it has been asked, how to display itself,
# the question it poses, the answer, and which learning
# sets that it belongs to.


import time
from PosedQuestionSequence import PosedQuestionSequence

class FlashCardItem:
  def __init__(self):
    self.questionText = None
    self.answerText = None
    self.history = PosedQuestionSequence()
    self.lastAskTime = 0

  def PrintQuestion(self):
    self.lastAskTime = time.time()
    print 'Question:', self.questionText

  def PrintAnswer(self):
    print 'Correct Answer:', self.answerText

  def IsCorrectAnswer(self, answer):
    # TODO: somehow check if the answer given is
    # close to the answer saved.
    isCorrect = (answer == self.answerText)
    return isCorrect


  def Hash(self):
    return hash(self.questionText + self.answerText)
