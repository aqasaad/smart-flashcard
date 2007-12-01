#! /usr/bin/env python
#
# Author: Jack Hebert (jhebert@gmail.com)
#
# Manages the program. Thus responsible for loading
# previous question sequences, the current flashcards,
# gets the questions to ask, gets the responses and all
# that good good jazz.
#

class ProgramManager:
  def __init__(self):
    self.learner = Learner()
    self.sessionManager = SessionHistory() 
    self.cardParser = FlashCardParser()

  def Init(self):
    flashcards = self.cardParser.ParseFile('')
    history = self.sessionManager.LoadSession('')
    flashcards.SetHistory(history)
    self.learner.SetCards(flashcards)

  def Start(self):
    # TODO: What would we do here?
    print 'Starting the flashcard session!'
    while(True):
      self.AskQuestion()
    self.Stop()


  def AskQuestion(self):
    self.learner.AskAQuestion()
    # TODO: grab the input response
    answer = ''
    self.learner.UpdateForAnswer(answer)

  def Stop(self):
    self.sessionManager.SaveSession(self.flashcards, '')
    # TODO: save the session history

