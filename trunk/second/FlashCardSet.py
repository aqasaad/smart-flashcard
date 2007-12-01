#! /usr/bin/env python
#
# Author: Jack Hebert (jhebert@gmail.com)
#
# This class will represent a group of flashcards
# as a single learning item.


import random

class FlashCardSet:
  def __init__(self, flashcards):
    self.flashcards = flashcards
    self.history = PosedQuestionSequence()
    self.lastQuestion = None

  def SetHistory(self, questionSequence):
    self.histpry = questionSequence()

  def AskQuestion(self, question):
    self.lastQuestionAsked = question
    question.PrintQuestion()

  def UpdateForAnswer(self, answer):
    self.history.UpdateForAnswer(self.lastQuestion, answer)
    question.history.UpdateForAnswer(question, answer)

  def ChooseRandomQuestion(self):
    num = random.randint(0, len(self.flashcards)-1)
    return self.flashcards[num]

  def ChooseLastAskedQuestion(self):
    return self.lastQuestion

  def ChooseEasiestQuestion(self):
    pass
    # TODO: Implement this.

  def ChooseHardestQuestion(self):
    pass
    # TODO: Implement this.

