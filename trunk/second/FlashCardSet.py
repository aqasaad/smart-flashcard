#! /usr/bin/env python
#
# Author: Jack Hebert (jhebert@gmail.com)
#
# This class will represent a group of flashcards
# as a single learning item.


class FlashCardSet:
  def __init__(self, flashcards):
    self.flashcards = flashcards
    self.history = PosedQuestionSequence()

  def SetHistory(self, questionSequence):
    self.histpry = questionSequence()

  def AskQuestion(self, question):
    question.PrintQuestion()

  def UpdateForAnswer(self, question, answer):
    self.history.UpdateForAnswer(question, answer)
    question.history.UpdateForAnswer(question, answer)

  def ChooseRandomQuestion(self):
    pass
    # TODO: Implement this.

  def ChooseLastAskedQuestion(self):
    pass
    # TODO: Implement this.

  def ChooseEasiestQuestion(self):
    pass
    # TODO: Implement this.

  def ChooseHardestQuestion(self):
    pass
    # TODO: Implement this.

