#! /usr/bin/env python
#
# Author: Jack Hebert (jhebert@gmail.com)
#
# This class will represent a group of flashcards
# as a single learning item.


import random
from PosedQuestionSequence import PosedQuestionSequence

class FlashCardSet:
  def __init__(self, flashcards):
    self.flashcards = flashcards
    self.history = PosedQuestionSequence()
    self.lastQuestion = None

  def SetHistory(self, questionSequence):
    self.history = questionSequence

  def AskQuestion(self, question):
    self.lastQuestion = question
    freq = self.history.CorrectQuestionFreq(question.Hash())
    globalFreq = self.history.CorrectFrequency()
    print 'Correct freq:', freq
    print 'Set correct freq:', globalFreq
    question.PrintQuestion()

  def UpdateForAnswer(self, answer):
    question = self.lastQuestion
    isCorrect = question.IsCorrectAnswer(answer)
    if (isCorrect):
      print '  Correct!'
    else:
      question.PrintAnswer()
    self.history.UpdateForAnswer(question, answer)
    question.history.UpdateForAnswer(question, answer)

  def ChooseRandomQuestion(self):
    num = random.randint(0, len(self.flashcards)-1)
    return self.flashcards[num]

  def ChooseLastAskedQuestion(self):
    return self.lastQuestion

  def ChooseEasiestQuestion(self):
    maxFreq, bestQuestion = -1, self.ChooseRandomQuestion()
    for question in self.flashcards:
      currFreq = self.history.CorrectQuestionFreq(question.Hash())
      if (currFreq > maxFreq):
        maxFreq, bestQuestion = currFreq, question
    return bestQuestion

  def ChooseHardestQuestion(self):
    lowestFreq, bestQuestion = 1, self.ChooseRandomQuestion()
    for question in self.flashcards:
      currFreq = self.history.CorrectQuestionFreq(question.Hash())
      if (currFreq < lowestFreq):
        lowestFreq, bestQuestion = currFreq, question
    return bestQuestion

  def ChooseRandomHardQuestion(self):
    pass
    # TODO: Wait towards a hard card but still choose
    # randomly from the set.

