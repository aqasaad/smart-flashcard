#! /usr/bin/env python
#
# Author: Jack Hebert (jhebert@gmail.com)
#
# This class will represent a group of flashcards
# as a single learning item.


class FlashCardSet:
  def __init__(self):
    self.flashcards = []
    self.history = None

  def AskQuestion(self, question):
    question.PrintQuestion()

  def UpdateForAnswer(self, question, answer):
    self.history.UpdateForAnswer(question, answer)
    question.history.UpdateForAnswer(question, answer)

  def ChooseRandomQuestion(self):
    pass

  def ChooseLastAskedQuestion(self):
    pass

  def ChooseEasiestQuestion(self):
    pass

  def ChooseHardestQuestion(self):
    pass

