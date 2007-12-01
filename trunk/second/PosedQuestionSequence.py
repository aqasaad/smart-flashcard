#! /usr/bin/env python
#
# Author: Jack Hebert (jhebert@gmail.com)
#
# A sequence of question posings - either for a single
# Flashcard or for a FlashcardSet.
#
# TODO: Any more methods needed for scoring that I
# should put in this class?

import time

class PosedQuestionSequence:
  def __init__(self):
    self.questionSequence = []

  def AddItem(self, question, time, answer):
    toAdd = PosedQuestion()
    toAdd.question = question
    toAdd.elapsedTime = time
    toAdd.correct = question.IsCorrectAnswer(answer)
    toAdd.answer = answer

  def UpdateForAnswer(self, question, answer):
    oldTime = question.lastAskTime
    currTime = time.time()
    timeDiff = currTime - oldTime
    self.AddItem(question, timeDiff, answer)

  def GetCorrectFrequency(self):
    # TODO: Implement this.
    pass



