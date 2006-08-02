#! /usr/bin/env python


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
    print 'Saving history . . .'
    f = open('.history', 'w')
    for word in history:
        toWrite = ' '.join([str(a) for a in history[word]])
        #print 'toAdd: '+str(toWrite)
        f.write(str(word) + ' : ' + toWrite + '\n')        
    f.close()


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

