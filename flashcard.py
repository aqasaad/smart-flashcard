#! /usr/bin/env python

import sys
import random
import time
import particleFilter
import gaussProcess
PRINT_PROB = True



#parse the input file data into words and definitions
def parseData(lines):
    toReturn = []
    for line in lines:
        split = line.find('-')
        if(split==-1):
            continue
        word = line[:split].strip()
        defn = line[split+1:].strip()
        if((len(word)>1) & (len(defn)>1)):
            toReturn.append((word,convString(word),convString(defn)))
    return toReturn

def askWord(Uword):
    print Uword
    if(PRINT_PROB):
        print prevProb
    user = raw_input('definition: ')



#loop until the user types 'quit'
def loop(items):
    user, words, result = '', {}, []
    maxRange, curRange = len(items), 5
    for word in items:
        words[word[0]] = None
    history, count = loadHistory(words)
    particleFilters, gauss = initLearning(history)
    pos, neg = gauss.binDataPoints(10)
    while(user != 'quit'):
        count += 1
        if(sum(result[-curRange:])*2 > curRange):
            curRange = curRange + 5
        index = min(len(items), int(random.random()*curRange))
        item = items[index]
        word, Uword, defn = item
        askWord(Uword)
        prevProb = particleFilters[word].getBestEstimate()

        if(user == 'quit'):
            break
        outCome = getStringMatch(user, defn)
        if(outCome == 1):
            print 'Correct!'
        else:
            print defn
        history[word].append((count,outCome))
        gauss.addDataPoint(word, prevProb, outCome)
        particleFilters[word].factorOutcome(outCome, gauss)
        print 'thingy:'+str(gauss.getResultantProb(prevProb, outCome))
        result.append(outCome)
        time.sleep(1)
        if(PRINT_PROB):
            print particleFilters[word].getBestEstimate()
        print '****'
    saveHistory(history)


def initLearning(history):
    toReturn = {}
    gauss = gaussProcess.gaussProcess()
    for word in history:
        p = particleFilter.particleFilter(1000)
        items = history[word]
        for item in items:
            try:
                count, result = item
                prob = p.getBestEstimate()
                gauss.addDataPoint(word, prob, result)
                print 'prob:'+str(prob)
                print 'result:'+str(result)
                print 'factoring:'+str(word)+':'+str(result)
                p.factorOutcome(result, gauss)
            except:
                continue
        toReturn[word] = p
    return (toReturn, gauss)


def loadHistory(words):
    toReturn, maxCount = {}, 0
    for word in words:
        toReturn[word] = []
    try:
        data = open('.history').read().split('\n')
    except:
        data = []
    for line in data:
        if(len(line)<3):
            continue
        word, items = line.split(' : ')
        if(len(items)<3):
            continue
        if(not(word in words)):
            continue
        for item in items.split('('):
            try:
                first = int(item[:item.find(',')])
                second = int(item[item.find(',')+2 : item.find(')')])
                maxCount = max(first, maxCount)
                toReturn[word].append((first, second))
            except:
                print 'item: '+str(item)
    return (toReturn, maxCount)



def saveHistory(history):
    f = open('.history', 'w')
    for word in history:
        toWrite = ' '.join([str(a) for a in history[word]])
        #print 'toAdd: '+str(toWrite)
        f.write(str(word) + ' : ' + toWrite + '\n')        
    f.close()



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
    #if(w1==w2):
    #    return 1
    #else:
    #    return 0


def getWordMatch(a,b):
    if((a=='') | (b=='')):
        return False
    na = a.lower()
    nb = b.lower()
    return (na == nb)


#convert the input data to unicode
#e/, e\, e^, a^ are currently matched
def convString(string):
    toReturn = []
    for s in string:
        if(s=='/'):
            if(toReturn[-1]=='e'):
                toReturn[-1]=unichr(233)
        elif(s=='\\'):
            if(toReturn[-1]=='e'):
                toReturn[-1]=unichr(232)
        elif(s=='^'):
            if(toReturn[-1]=='e'):
                toReturn[-1]=unichr(234)
            elif(toReturn[-1]=='a'):
                toReturn[-1]=unichr(226)
        else:
            toReturn.append(s) 
    return unicode(''.join(toReturn))


#open .flashcard and see if a similar file name has been entered before
def resolveFileName(name):
    possible = []
    try:
        data = [a[5:] for a in open('.flashcard').read().split('\n') if(a.find('file:')>-1)]
    except:
        data = []
    for item in data:
        if(item.find(name)>-1):
            possible.append(item)
    if(len(possible)>0):
       toReturn = possible[0]
    else:
        toReturn = name
    try:
        open(name).read()
        file = open('.flashcard','a')
        file.write('\nfile:'+name)
        file.close()
    except:
        print ''
    return toReturn


#main program loop
def main():
    runQuestions()



def runQuestions():
    if(len(sys.argv)<2):
        print 'please specify an input file!'
    fileName = sys.argv[1]
    name = resolveFileName(fileName)
    data = open(name).read().split('\n')
    items = parseData(data)
    loop(items)

    
    



main()

