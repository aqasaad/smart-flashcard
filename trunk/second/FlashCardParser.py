#! /usr/bin/env python
#
# Author: Jack Hebert (jhebert@gmail.com)
#
# This class is responsible for parsing question/answer
# files.
#
# TODO (jhebert): Each answer file should be able to
# specify a type, and if not default to the method
# specified here - allowing future xml and html more easily.


from FlashCardItem import FlashCardItem
from FlashCardSet import FlashCardSet

class FlashCardParser:
  def __init__(self):
    pass

  def ParseFile(self, fileName):
    flashcards = []
    lines = open(fileName).read().split('\n')
    for line in lines:
      if(len(line) < 3):
        continue
      try:
        question, answer = line.split('<@>')
	newCard = self.CreateFlashCard(question, answer)
        flashcards.append(newCard)
      except ValueError:
        print 'Could not parse line:', line
    flashCardSet = FlashCardSet(flashcards)
    return flashCardSet

  def CreateFlashCard(self, question, answer):
    flashcard = FlashCardItem()
    flashcard.questionText = question.strip()
    flashcard.answerText = answer.strip()
    return flashcard
