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
        flashcards.append(question, answer)	
      except ParseError:
        print 'Could not parse line:', line
    return flashcards


  def CreateFlashCard(self, question, answer):
    flashcard = FlashCardItem()
    flashcard.questionText = question
    flashcard.answerText = answer
    return flashcard
