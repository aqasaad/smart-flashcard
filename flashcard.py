#! /usr/bin/env python

import sys
import random
import time
import particleFilter
import gaussProcess
import fileHandlers
PRINT_PROB = True




def askWord(Uword, defn, prevProb):
    print Uword
    if(PRINT_PROB):
        print prevProb
    user = raw_input('definition: ')
    if(user == 'quit'):
         return -1
    outCome = getStringMatch(user, defn)
    if(outCome == 1):
        print 'Correct!'
    else:
        print defn
        time.sleep(1)
    return outCome



#loop until the user types 'quit'
def loop(items):
    user, words, result = '', {}, []
    maxRange, curRange = len(items), 5
    for word in items:
        words[word[0]] = None
    history, count = fileHandlers.loadHistory(words)
    oldCount = count
    particleFilters, gauss = initLearning(history)
    #pos, neg = gauss.binDataPoints(10)
    #print 'pos:'+str(pos)
    #print 'neg:'+str(neg)
    while(user != 'quit'):
        count += 1
        if(sum(result[-curRange:])*2 > curRange):
            curRange = curRange + 5
        index = min(len(items)-1, int(random.random()*curRange))
        item = items[index]
        word, Uword, defn = item
        prevProb = particleFilters[word].getBestEstimate()
        posChange = particleFilters[word].getPotentialOutcome(1, gauss, count)
        negChange = particleFilters[word].getPotentialOutcome(0, gauss, count)
        print 'potential pos change: ' + str(posChange)
        print 'potential neg change: ' + str(negChange)
        outCome = askWord(Uword, defn, prevProb) 
        if(outCome == -1):
            break
        history[word].append((count,outCome))
        gauss.getBlankProb(prevProb, outCome, word, count)
        gauss.addDataPoint(word, prevProb, outCome, count)
        particleFilters[word].factorOutcome(outCome, gauss, count)
        #print 'thingy:'+str(gauss.getResultantProb(prevProb, outCome, count))
        result.append(outCome)
        if(PRINT_PROB):
            print particleFilters[word].getBestEstimate()
        print '****'
        # This shouldn't fuxor my histroy, right?
        if(count-oldCount > 10):
            fileHandlers.saveHistory(history)
            history, count = fileHandlers.loadHistory(words)
            oldCount = count
    fileHandlers.saveHistory(history)


def initLearning(history):
    print 'init learning'
    toReturn = {}
    gauss = gaussProcess.gaussProcess()
    for word in history:
        p = particleFilter.particleFilter(word, 1000)
        items = history[word]
        for item in items:
            try:
                count, result = item
                prob = p.getBestEstimate()
                gauss.addDataPoint(word, prob, result, count)
                print 'prob:'+str(prob)
                print 'result:'+str(result)
                print 'factoring:'+str(word)+':'+str(result)
                p.factorOutcome(result, gauss, count)
            except:
                continue
        toReturn[word] = p
    return (toReturn, gauss)




#return a numerical score for how well the user's input matches the definition
def getStringMatch(w1, w2):
    #This should decide how close the two words are to each other.
    w1s = [a.strip() for a in w1.split(',')]
    w2s = [a.strip() for a in w2.split(',')]
    for a in w1s:
        for b in w2s:
            if(getWordMatch(a,b)):
                return 1
    return 0



def getWordMatch(a,b):
    if((a=='') | (b=='')):
        return False
    na = a.lower()
    nb = b.lower()
    return (na == nb)





#main program loop
def main():
    runQuestions()



def runQuestions():
    if(len(sys.argv)<2):
        print 'please specify an input file!'
    fileName = sys.argv[1]
    name = fileHandlers.resolveFileName(fileName)
    data = open(name).read().split('\n')
    items = fileHandlers.parseData(data)
    loop(items)

    
    



main()

