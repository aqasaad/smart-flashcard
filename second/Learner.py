#! /usr/bin/env python
#
# Author: Jack Hebert (jhebert@gmail.com)
#
# Manages the Flashcards and Learning experience.
#

class Learner:
  def __init__(self):
    self.flashCardSet = Noone
    self.knowledgeEstimator = None
    self.lastQuestion = None

  def SetCards(self, flashCardSet):
    self.flashCardSet = flashCardSet

  def AskAQuestion(self):
    toAsk = self.PickAQuestion()
    self.lastQuestion = toAsk
    toAsk.PrintQuestion()

  def PickAQuestion(self):
    question = self.flashCardSet.ChooseRandomQuestion()

  def UpdateForAnswer(self, answer):
    self.flasCardSet.UpdateForAnswer(question, answer)

