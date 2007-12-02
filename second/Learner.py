#! /usr/bin/env python
#
# Author: Jack Hebert (jhebert@gmail.com)
#
# Manages the Flashcards and Learning experience.
#


class Learner:
  def __init__(self):
    self.allFlashCards = None
    self.workingSet = None
    self.knowledgeEstimator = None

  def SetCards(self, flashCardSet):
    self.allFlashCards = flashCardSet
    self.ChooseWorkingSet()

  def ChooseWorkingSet(self):
    self.workingSet = self.allFlashCards

  def AskAQuestion(self):
    toAsk = self.PickAQuestion()
    print '*****'
    self.workingSet.AskQuestion(toAsk)

  def PickAQuestion(self):
    question = self.workingSet.ChooseRandomQuestion()
    #question = self.workingSet.ChooseHardestQuestion()
    #question = self.workingSet.ChooseEasiestQuestion()
    return question

  def UpdateForAnswer(self, answer):
    self.workingSet.UpdateForAnswer(answer)

