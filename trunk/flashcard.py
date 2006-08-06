#! /usr/bin/env python

import sys
import random
import time
import particleFilter
import gaussProcess
import fileHandlers


class flashcard:


    def __init__(self):
        #should the user be informed of probabilities?
        self.PRINT_PROB = True
        #A mapping of words to particle filters
        self.particleFilters = {}
        #A learned for all words
        self.gauss = None
        #A hash of all words and their definitions
        self.flashItems = None
        #Save the previous word asked.
        self.prevWord = ""
        self.improveList = []



    # Ask the user a word and print the definition if incorrect
    def askWord(self, word, Uword, defn, prevProb):
        self.prevWord = word
        print Uword
        if(self.PRINT_PROB):
            print prevProb
        user = raw_input('definition: ')
        if(user == 'quit'):
            return -1
        outCome = self.getStringMatch(user, defn)
        if(outCome == 1):
            print 'Correct!'
        else:
            print defn
            time.sleep(1)
        return outCome


    def chooseWord(self, count):
        return self.chooseImproveWord(count)
        #return self.chooseImprovementWord(count)
        #return self.chooseRandomWord()

    def chooseRandomWord(self):
        i = random.random()*len(self.flashItems)
        return self.flashItems[i]


    def chooseImproveWord(self, count):
        for i in range(10)[1:]:
            val, item = self.improveList[-i]
            v = self.__getExpectedImprovement__(item[0], count)
            self.improveList[-i] = (v, item)
        self.improveList.sort()
        val, item = self.improveList[-1]
        print self.improveList[-5:]
        return item


    # Choose which word to ask the user next
    # This should be done with a heap, save some state from previous runs. Update the
    # top so many words each time, not all!
    def chooseImprovementWord(self, count):
        maxVal, maxItem = -99999, ''
        for item in self.flashItems:
            word = item[0]
            #prob = self.particleFilters[word].getBestEstimate()
            #posChange = self.particleFilters[word].getPotentialOutcome(1, self.gauss, count)
            #negChange = self.particleFilters[word].getPotentialOutcome(0, self.gauss, count)
            #v1 = prob * self.valueOfProb(posChange) + (1-prob) * self.valueOfProb(negChange)
            v = self.__getExpectedImprovement__(word, count)
            #v2 = self.valueOfProb(prob)
            #delta = v1-v2
            if((v > maxVal) & (self.prevWord != word)):
                print 'delta:'+str(v)
                #print 'maxVal:'+str(maxVal)
                print 'word:'+str(word)
                maxVal = v
                maxItem = item
        return maxItem

    def __initImproveList__(self, count):
        haveDone = {}
        print 'Initing the improvement data structure . . .'
        for item in self.flashItems:
            word = item[0]
            if(word in haveDone):
                continue
            else:
                haveDone[word] = None
            v = self.__getExpectedImprovement__(word, count)
            self.improveList.append((v, item))
        self.improveList.sort()

    def __getExpectedImprovement__(self, word, count):
        prob = self.particleFilters[word].getBestEstimate()
        posChange = self.particleFilters[word].getPotentialOutcome(1, self.gauss, count)
        negChange = self.particleFilters[word].getPotentialOutcome(0, self.gauss, count)
        v1 = prob * self.valueOfProb(posChange) + (1-prob) * self.valueOfProb(negChange)
        v2 = self.valueOfProb(prob)
        return v1-v2

    # Define a value for the probability distribution.
    # It currently only scores for one probability, but should
    # take the entire distribution into account.
    def valueOfProb(self, p):
        if(p<.4):
            return -5
        elif(p < .6):
            return -1
        elif(p < .75):
            return 1
        else:
            return 3

        #Do I even need the result list? Is it not just using the history hash?
    # Main loop of the program, ask words, update distributions, save results.
    #loop until the user types 'quit'
    def loop(self):
        user, words, result = '', {}, []
        for word in self.flashItems:
            words[word[0]] = None
        history, count = fileHandlers.loadHistory(words)
        oldCount = count
        self.initLearning(history)
        while(user != 'quit'):
            count += 1
            item = self.chooseWord(count)
            word, Uword, defn = item
            prevProb = self.doPreInfo(word, count)
            outCome = self.askWord(word, Uword, defn, prevProb) 
            if(outCome == -1):
                break
            history[word].append((count,outCome))
            result.append(outCome)
            self.doPostInfo(prevProb, outCome, word, count)
            # This shouldn't fuxor my histroy, right?
            if(count-oldCount > 10):
                fileHandlers.saveHistory(history)
                history, count = fileHandlers.loadHistory(words)
                oldCount = count
        fileHandlers.saveHistory(history)


    # Calculate prior probability, possibly display some info to user.
    def doPreInfo(self, word, count):
        prevProb = self.particleFilters[word].getBestEstimate()
        if(self.PRINT_PROB):
            posChange = self.particleFilters[word].getPotentialOutcome(1, self.gauss, count)
            negChange = self.particleFilters[word].getPotentialOutcome(0, self.gauss, count)
            print 'potential pos change: ' + str(posChange)
            print 'potential neg change: ' + str(negChange)
        return prevProb

    # Add data to learner, update particle filter.
    def doPostInfo(self, prevProb, outCome, word, count):
        #print 'blankProb:'+str(self.gauss.getBlankProb(prevProb, outCome, word, count))
        self.particleFilters[word].factorOutcome(outCome, self.gauss, count)
        self.gauss.addDataPoint(word, prevProb, outCome, count)
        if(self.PRINT_PROB):
            print self.particleFilters[word].getBestEstimate()
        print '****'


    # Create the learning data structures, incorporate previous results to distributions.
    def initLearning(self, history):
        print 'init learning'
        toReturn, count = {}, 0
        self.gauss = gaussProcess.gaussProcess()
        for word in history:
            p = particleFilter.particleFilter(word, 500)
            items = history[word]
            for item in items:
                try:
                    count, result = item
                    prob = p.getBestEstimate()
                    self.gauss.addDataPoint(word, prob, result, count)
                    print 'prob:'+str(prob)
                    print 'result:'+str(result)
                    print 'factoring:'+str(word)+':'+str(result)
                    p.factorOutcome(result, self.gauss, count)
                except:
                    continue
            toReturn[word] = p
        self.particleFilters = toReturn
        self.__initImproveList__(count+1)



    #return a numerical score for how well the user's input matches the definition
    def getStringMatch(self, w1, w2):
        #This should decide how close the two words are to each other.
        w1s = [a.strip() for a in w1.split(',')]
        w2s = [a.strip() for a in w2.split(',')]
        for a in w1s:
            for b in w2s:
                if(self.getWordMatch(a,b)):
                    return 1
        return 0


    # Return True if individual words match
    def getWordMatch(self, a,b):
        if((a=='') | (b=='')):
            return False
        na = a.lower()
        nb = b.lower()
        return (na == nb)


    # Run the flashcard program
    def runQuestions(self):
        if(len(sys.argv)<2):
            print 'please specify an input file!'
        fileName = sys.argv[1]
        name = fileHandlers.resolveFileName(fileName)
        data = open(name).read().split('\n')
        self.flashItems = fileHandlers.parseData(data)
        self.loop()



#main program loop
def main():
    flash = flashcard()
    flash.runQuestions()



main()

