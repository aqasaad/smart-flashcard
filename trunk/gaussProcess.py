#! /usr/bin/env python


import random
import math

class gaussProcess:



    def __init__(self):
        self.dataPoints = [[], []]
        self.prevData = {}

    def addDataPoint(self, word, p, r):
        p = min(.9999, max(.0001, p))
        if(word in self.prevData):
            oldP, oldR = self.prevData[word]
            self.dataPoints[oldR].append((oldP, r))
        self.prevData[word] = (p, r)
        #self.dataPoints.append((p,r))


    def getResultantProb(self, pProb, outCome):
        sumWeights = 0.0
        sumResults = 0.0
        data = self.dataPoints[outCome]
        for item in data:
            nProb, result = item
            diff = nProb - pProb
            sigma = diff / .1
            w = math.e ** (-sigma*sigma)
            sumResults += w * result
            sumWeights += w
        return (sumResults / sumWeights) - pProb
            

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



    





