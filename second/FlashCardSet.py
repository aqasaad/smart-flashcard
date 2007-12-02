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
    freq = self.CorrectQuestionFreq(question.Hash())
    print 'Correct freq:', freq
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
    highestFreq, bestQuestion = -1, self.ChooseRandomQuestion()
    for question in self.flashcards:
      currFreq = self.CorrectQuestionFreq(question.Hash())
      if (currFreq > highestFreq):
        highestFreq, bestQuestion = currFreq, question
    return bestQuestion

  def ChooseHardestQuestion(self):
    lowestFreq, bestQuestion = 1, self.ChooseRandomQuestion()
    for question in self.flashcards:
      currFreq = self.CorrectQuestionFreq(question.Hash())
      if (currFreq < lowestFreq):
        lowestFreq, bestQuestion = currFreq, question
    return bestQuestion

  def CorrectFrequency(self):
    correctCount, totalCount = 0, 0
    for posedQuestion in self.history.questionSequence:
      totalCount += 1
      if (posedQuestion.correct):
        correctCount += 1
    if (totalCount == 0):
      return 0
    return float(correctCount) / totalCount

  def CorrectQuestionFreq(self, questionHash):
    correctCount, totalCount = 0, 0
    for posedQuestion in self.history.questionSequence:
      if (posedQuestion.questionHash != questionHash):
        continue
      totalCount += 1
      if (posedQuestion.correct):
        correctCount += 1
    if (totalCount == 0):
      return 0
    return float(correctCount) / totalCount
