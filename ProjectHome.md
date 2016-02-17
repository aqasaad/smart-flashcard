This system uses probabilistic techniques to estimate a user's knowledge and intelligently ask different flashcard definitions.

The problem is represented as such: At each point in time there is a probability distribution describing a user's chance of defining a word correctly. By asking the user to provide the definition, you observe that distribution. Then telling the user that they are right or wrong affects the distribution.

The probability distribution for a user to correctly answer each word is calculated via particle filtering.

The resultant change in probability distribution from answering a definition is learned, and assumed to be dependent upon: previous probability of answering correctly, whether the user answered correctly, and how long it had been since the word had been previously asked. Thus a user is (hypotheticly) likely to learn more if frequently asked a word, and the amount learned varies depending on how well they already know the word.

With that probabilistic reasoning in place, a value function is defined for probability distributions. The program then finds it very valuable to know a word well, and painful to know a word poorly. The program then selects the next word to ask by greedily choosing the word that is most likely to increase the total value function (probabilistically of course).

The implementation is in python, still slow, lacks a GUI, and could use some more words to ask (I have learned them all through debugging . . .).


The program architecture still needs to be fitted with the idea of a 'working set' of words, which define those over which the value function is computed. Thus, the program is able to ask the user new words incrementally rather than the entire dictionary at once.


