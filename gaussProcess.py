#! /usr/bin/env python


import random
import math

class gaussProcess:



    def __init__(self):
        # These two lists hold the collected data points.
        # The first holds incorrect (user) results and the
        # second holds correct (user) results.
        # The data is in the form of tuples:
        # (estimated probability of being correctly answered,
        # (whether the user did answer correctly,
        # how many other words had been asked since previously
        # asking this word).
        self.dataPoints = [[], []]
        # This is a hash of words to tuples of probability, answer
        # result, and the iteration count of the flashCard loop.
        # This structure exists so that 'dataPoints' structure can
        # be correctly maintained.
        self.prevData = {}
        self.loadedHistory = False


    def saveHistory(self):
        file = open('gauss.history','w')
        for item in self.dataPoints[0]:
            a,b,c = item
            file.write('0'+' '+str(a)+' '+str(b)+' '+str(c)+'\n')
        for item in self.dataPoints[1]:
            a,b,c = item
            file.write('1'+' '+str(a)+' '+str(b)+' '+str(c)+'\n')
        file.close()

    def loadHistory(self):
        if(self.loadedHistory):
            return
        self.loadedHistory = True
        try:
            data = open('gauss.history').read().split('\n')
            for line in data:
                if(len(line)<3):
                    continue
                first, prob, result, blank = line.split(' ')
                self.dataPoints[int(first)].append((float(prob), int(result), int(blank)))
        except:
            print 'Failed to read in history'

                       
    # Add a data point to the collection. This allows a relation to be
    # built between esitamated probability, previously learning, and current
    # answering of definitions.
    def addDataPoint(self, word, p, r, count):
        p = min(.999999, max(.000001, p))
        if(word in self.prevData):
            oldP, oldR, oldCount = self.prevData[word]
            self.dataPoints[oldR].append((oldP, r, count-oldCount))
        self.prevData[word] = (p, r, count)


    # Get the predicted probability weigted by normal distributions
    # based off of the learned data points. Factors on outCome, probability
    # estimate.
    def getResultantProb(self, pProb, outCome, word, count):
        sumWeights, sumResults = 0.0, 0.0
        data = self.dataPoints[outCome]
        for item in data:
            nProb, result, deltaCount = item
            diff = nProb - pProb
            sigma = diff / .1
            w = math.e ** (-sigma*sigma)
            sumResults += w * result
            sumWeights += w
        if(sumWeights==0):
            return pProb
        else:
            return (sumResults / sumWeights)


    # Like above, but also incorporates number of iterations
    # since tihs word was last asked - hence to incorporate
    # gains via short term memory and such.
    def getBlankProb(self, pProb, outCome, word, count):
        sumResults2, sumWeights2 = 0.0, 0.0
        for item in self.dataPoints[outCome]:
            try:
                nProb, result, deltaCount = item
                diff = nProb - pProb
                diffCount = abs(deltaCount) - abs(self.prevData[word][2] - count)
                sigma = diff / .05
                sigmaCount = diffCount / 6
                w = math.e ** (-(sigma*sigma + sigmaCount*sigmaCount))
                sumResults2 += w * result
                sumWeights2 += w
                #w1 = math.e ** (-sigma*sigma)
                #w2 = math.e ** (-sigmaCount*sigmaCount)
                #sumResults2 += w1*w2*result
                #sumWeights2 += w1*w2
            except:
                continue
        if(sumWeights2==0):
            return pProb
        else:
            return (sumResults2 / sumWeights2)



    # I think that this is only called from a commented
    # portion of code in flashcard.py
    # So it really isn't too important.
    def binDataPoints(self, nBins):
        pos = []
        neg = []
        for i in range(nBins):
            pos.append([0, 0])
            neg.append([0, 0])
        for point in self.dataPoints[0]:
            try:
                prob, result = point
                bin = int(prob * nBins)
                neg[bin][result] += 1
            except:
                print 'point:'+str(point)
        for point in self.dataPoints[1]:
            try:
                prob, result = point
                bin = int(prob * nBins)
                pos[bin][result] += 1
            except:
                print 'point:'+str(point)
        for i in range(nBins):
            pos[i].append(float(pos[i][1]) / (pos[i][0] + pos[i][1] + 1))
            neg[i].append(float(neg[i][1]) / (neg[i][0] + neg[i][1] + 1))
        return (pos, neg)



    





