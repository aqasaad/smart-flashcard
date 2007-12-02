#! /usr/bin/env python
#
# Author: Jack Hebert (jhebert@gmail.com)
#
# Represents a single posing of a Flashcard to a user.
#


class PosedQuestion:
  def __init__(self):
    self.questionHash = None
    self.elapsedTime = None
    self.correct = False
    self.answer = None
