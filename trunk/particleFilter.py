#! /usr/bin/env python


import random
import gaussProcess

class particleFilter:


    def __init__(self, n):
        #Number of particles in this particleFilter
        self.numParticles = n
        #Array to store particle locations
        self.particleArray = [0] * self.numParticles
        for i in range(len(self.particleArray)):
            self.particleArray[i] = random.random()

    def getPotentialOutcome(self, outCome, gauss):
        particles = self.__reSample__(self.__getLikelihoods__(outCome), gauss, outCome)
        return self.__bestEstimateHelper__(particles)

    def factorOutcome(self, outCome, gauss):
        particles = self.__reSample__(self.__getLikelihoods__(outCome), gauss, outCome)
        self.__updateParticleArray__(particles)

    def __getLikelihoods__(self, outCome):
        toReturn = []
        # if outCome = 0, then want 1 - p
        # if outCome = 1, then want p
        #
        for p in self.particleArray:
            if(outCome == 0):
                toReturn.append(1-p)
            else:
                toReturn.append(p)
        return toReturn

    def __updateParticleArray__(self, particles):
        self.particleArray = particles

    def __reSample__(self, likelihoods, gauss, outCome):
        toReturn = []
        s = sum(likelihoods)
        delta = s / (self.numParticles+1)
        start = random.random() * delta
        i,j = 0,0
        pointerSum = start
        accumSum = 0
        while(j < self.numParticles):
            pointerSum += delta
            while(accumSum < pointerSum):
                accumSum += likelihoods[i]
                i += 1
            newPart = self.particleArray[i-1] + random.gauss(0,.08)
            newPart = min(.9999, max(.0001, newPart))
            change = gauss.getResultantProb(self.particleArray[i-1], outCome)
            if(abs(change) < .3):
                newPart += change
            else:
                newPart += .3 * change / abs(change)
            newPart = min(.9999, max(.0001, newPart))
            toReturn.append(newPart)
            j += 1
        #self.particleArray = toReturn
        return toReturn

    def getBestEstimate(self):
        return self.__bestEstimateHelper__(self.particleArray)

    #This really should be done better!
    #I could choose the best particle.
    #Or I could bin and choose the heaviest bin!
    def __bestEstimateHelper__(self, particles):
        hist = [0]*20
        for p in particles:
            hist[min(19,int(p*20))] += 1
        #print hist
        maxI = 0
        for i in range(20):
            if(hist[i]==max(hist)):
                maxI = i
        aSum, aCount = 0,0
        for p in particles:
            if(min(19,int(p*20)) == maxI):
                aSum += p
                aCount += 1
        if(aCount==0):
            print maxI
            print hist
        return aSum / aCount



