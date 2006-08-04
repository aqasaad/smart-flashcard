#! /usr/bin/env python


import random
import math

class gaussProcess:



    def __init__(self):
        self.dataPoints = [[], []]
        self.prevData = {}


    def addDataPoint(self, word, p, r, count):
        p = min(.999999, max(.000001, p))
        if(word in self.prevData):
            oldP, oldR, oldCount = self.prevData[word]
            self.dataPoints[oldR].append((oldP, r, count-oldCount))
            #self.dataPoints[2].append((oldP, r, count-oldCount))
        self.prevData[word] = (p, r, count)
        #self.dataPoints.append((p,r))


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


    def getBlankProb(self, pProb, outCome, word, count):
        sumResults2, sumWeights2 = 0.0, 0.0
        for item in self.dataPoints[outCome]:
            try:
                nProb, result, deltaCount = item
                diff = nProb - pProb
                diffCount = abs(deltaCount) - abs(self.prevData[word][2] - count)
                sigma = diff / .05
                sigmaCount = diffCount / 6
                w1 = math.e ** (-sigma*sigma)
                w2 = math.e ** (-sigmaCount*sigmaCount)
                sumResults2 += w1*w2*result
                sumWeights2 += w1*w2
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



    





