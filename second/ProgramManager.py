#! /usr/bin/env python
#
# Author: Jack Hebert (jhebert@gmail.com)
#
# Manages the program. Thus responsible for loading
# previous question sequences, the current flashcards,
# gets the questions to ask, gets the responses and all
# that good good jazz.
#


from FlashCardParser import FlashCardParser
from Learner import Learner
from SessionHistory import SessionHistory


class ProgramManager:
  def __init__(self):
    self.learner = Learner()
    self.sessionManager = SessionHistory() 
    self.cardParser = FlashCardParser()

  def Init(self):
    flashcards = self.cardParser.ParseFile('sample.dat')
    history = self.sessionManager.LoadSession('session.history')
    flashcards.SetHistory(history)
    self.learner.SetCards(flashcards)

  def Start(self):
    print 'Starting the flashcard session!'
    while(True):
      quit = self.AskQuestion()
      if (quit):
        break
    self.Stop()


  def AskQuestion(self):
    self.learner.AskAQuestion()
    answer = raw_input('Answer: ')
    if (answer == 'exit'):
      return True
    self.learner.UpdateForAnswer(answer)
    return False

  def Stop(self):
    print 'Ending the flashcard session...'
    self.sessionManager.SaveSession(self.flashcards, 'session.history')


def main():
  p = ProgramManager()
  p.Init()
  p.Start()


if (__name__ == '__main__'):
  main()