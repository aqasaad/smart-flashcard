#! /usr/bin/env python

import sys
import random
import time
import particleFilter
import gaussProcess
import fileHandlers
import stringMatch


class flashcard:


    def __init__(self):
        #should the user be informed of probabilities?
        self.PRINT_PROB = False
        #A mapping of words to particle filters
        self.particleFilters = {}
        #A learned for all words
        self.gauss = None
        #A hash of all words and their definitions
        self.flashItems = None
        #Save the previous word asked.
        self.prevWord = ""
        #The previous item asked.
        self.prevItem = None
        #A tuple list of (possible improvement, word item)
        self.improveList = []
        #ID for the vocab file being used
        self.ident = ''
        self.gauss = gaussProcess.gaussProcess()
        self.stringMatch = stringMatch.stringMatch()



    # Ask the user a word and print the definition if incorrect
    def askWord(self, word, Uword, defn, prevProb):
        self.prevWord = word
        print Uword
        if(self.PRINT_PROB):
            print prevProb
        user = raw_input('definition: ')
        if(user == 'quit'):
            return -1
        outCome = self.stringMatch.getStringMatch(user, defn)
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
            if(i>len(self.improveList)):
                continue
            val, item = self.improveList[-i]
            v = self.__getExpectedImprovement__(item[0], count)
            self.improveList[-i] = (v, item)
        self.improveList.sort()
        val, item = self.improveList[-1]
        if(item == self.prevItem):
            val, item = self.improveList[-2]
        for item in self.improveList[-5:]:
            val, i = item
            print str(val) + ' : ' + str(i[0])
        self.prevItem = item
        return item



    def __initImproveList__(self, count):
        itemCount, total = 0, len(self.flashItems)
        print 'Initing the improvement data structure . . .'
        for item in self.flashItems:
            itemCount += 1
            print str(itemCount) + ' : ' + str(total)
            word = item[0]
            v = self.__getExpectedImprovement__(word, count)
            self.improveList.append((v, item))
        self.improveList.sort()


    def __getExpectedImprovement__(self, word, count):
        particle = self.particleFilters[word]
        prob = particle.getBestEstimate()
        p = particle.evalPotentialDistrib(1, self.gauss, count)
        n = particle.evalPotentialDistrib(0, self.gauss, count)
        v1 = prob * p + (1-prob)*n
        v2 = particle.evalCurrentDistrib()
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
        elif(p < .9):
            return 3
        else:
            return 8


        #Do I even need the result list? Is it not just using the history hash?
    # Main loop of the program, ask words, update distributions, save results.
    #loop until the user types 'quit'
    def loop(self):
        user, words= '', {}
        for word in self.flashItems:
            words[word[0]] = None
        history, count = fileHandlers.loadHistory(self.ident, words, self.gauss)
        oldCount = count
        self.initLearning(history)
        #self.gauss.listData()
        while(user != 'quit'):
            count += 1
            item = self.chooseWord(count)
            word, Uword, defn = item
            prevProb = self.doPreInfo(word, count)
            outCome = self.askWord(word, Uword, defn, prevProb) 
            if(outCome == -1):
                break
            history[word].append((count,outCome))
            self.doPostInfo(prevProb, outCome, word, count)
            # This shouldn't fuxor my histroy, right?
            if(count-oldCount > 10):
                fileHandlers.saveHistory(self.ident, history, self.gauss)
                history, count = fileHandlers.loadHistory(self.ident, words, self.gauss)
                oldCount = count
        fileHandlers.saveHistory(self.ident, history, self.gauss)


    # Calculate prior probability, possibly display some info to user.
    def doPreInfo(self, word, count):
        prevProb = self.particleFilters[word].getBestEstimate()
        self.particleFilters[word].printHist()
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
        self.particleFilters[word].printHist()
        print '****'


    # Create the learning data structures, incorporate previous results to distributions.
    def initLearning(self, history):
        print 'init learning'
        toReturn, count = {}, 0
        for word in history:
            p = particleFilter.particleFilter(word, 500)
            items = history[word]
            for item in items:
                try:
                    count, result = item
                    prob = p.getBestEstimate()
                    p.factorOutcome(result, self.gauss, count)
                    #self.gauss.addDataPoint(word, prob, result, count)
                    print 'prob:'+str(prob)
                    print 'hist:'
                    p.printHist()
                    print 'result:'+str(result)
                    print 'factoring:'+str(word)+':'+str(result)
                except:
                    continue
            toReturn[word] = p
        self.particleFilters = toReturn
        self.__initImproveList__(count+1)





    # Run the flashcard program
    def runQuestions(self):
        if(len(sys.argv)<2):
            print 'please specify an input file!'
        fileName = sys.argv[1]
        #name = fileHandlers.resolveFileName(fileName)
        #data = open(name).read().split('\n')
        #self.flashItems = fileHandlers.parseData(data)
        self.ident, self.flashItems = fileHandlers.getFlashItems(fileName)
        
        self.loop()



#main program loop
def main():
    flash = flashcard()
    flash.runQuestions()



main()

