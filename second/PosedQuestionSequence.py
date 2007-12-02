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
from PosedQuestion import PosedQuestion


class PosedQuestionSequence:
  def __init__(self):
    self.questionSequence = []

  def AddItem(self, question, time, answer):
    toAdd = PosedQuestion()
    toAdd.questionHash = question.Hash()
    toAdd.elapsedTime = time
    toAdd.correct = question.IsCorrectAnswer(answer)
    toAdd.answer = answer
    self.questionSequence.append(toAdd)

  def UpdateForAnswer(self, question, answer):
    oldTime = question.lastAskTime
    currTime = time.time()
    timeDiff = currTime - oldTime
    self.AddItem(question, timeDiff, answer)

  def CorrectFrequency(self):
    correctCount, totalCount = 0, 0
    for posedQuestion in self.questionSequence:
      totalCount += 1
      if (posedQuestion.correct):
        correctCount += 1
    if (totalCount == 0):
      return 0
    return float(correctCount) / totalCount

  def CorrectQuestionFreq(self, questionHash):
    correctCount, totalCount = 0, 0
    for posedQuestion in self.questionSequence:
      if (posedQuestion.questionHash != questionHash):
        continue
      totalCount += 1
      if (posedQuestion.correct):
        correctCount += 1
    if (totalCount == 0):
      return 0
    return float(correctCount) / totalCount

