#! /usr/bin/env python


import random
import gaussProcess

class particleFilter:


    def __init__(self, word, n):
        #Variance when adding nose to selected particles in resampling.
        self.PARTICLE_VAR = .01
        #The word for this particle filter.
        self.word = word
        #Number of particles in this particleFilter
        self.numParticles = n
        #Array to store particle locations
        self.particleArray = [0] * self.numParticles
        #Init the particles into a uniform distribution.
        for i in range(len(self.particleArray)):
            self.particleArray[i] = random.random()


    #Return a estimate probability for the distribution after the 'outCome' event.
    def getPotentialOutcome(self, outCome, gauss, count):
        particles = self.__reSample__(self.__getLikelihoods__(outCome), gauss, outCome, count)
        return self.__bestEstimateHelper__(particles)


    #Factor the 'outCome' event into the probability distribution and save the results.
    def factorOutcome(self, outCome, gauss, count):
        particles = self.__reSample__(self.__getLikelihoods__(outCome), gauss, outCome, count)
        self.__updateParticleArray__(particles)


    #Return the likelihoods for each particle for the event 'outCome'
    def __getLikelihoods__(self, outCome):
        # if outCome = 0, then want 1 - p
        # if outCome = 1, then want p
        return [(1-outCome)+(2*outCome-1)*p for p in self.particleArray]


    # Save 'particles' as the particleArray for this particleFilter
    def __updateParticleArray__(self, particles):
        self.particleArray = particles


    # Resample the particles according to their likelihoods.
    # This is done using a 'clock hand' type method. It is linear
    # in complexity and in the limit is just as good. See Dieter
    # Fox's CSE 473 slides Spring 2005, Robotics lecture.
    def __reSample__(self, likelihoods, gauss, outCome, count):
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
            newPart = self.particleArray[i-1] + random.gauss(0,self.PARTICLE_VAR)
            newPart = min(.999999, max(.000001, newPart))
            p = self.particleArray[i-1]
            change = gauss.getResultantProb(p, outCome, self.word, count) - p
            if(abs(change) < .3):
                newPart += change
            else:
                newPart += .3 * change / abs(change)
            newPart = min(.999999, max(.000001, newPart))
            toReturn.append(newPart)
            j += 1
        return toReturn


    # Outside method indirectly calling internal method
    # to determine the best estimate for the peak of this
    # distribution.
    def getBestEstimate(self):
        return self.__bestEstimateHelper__(self.particleArray)


    # Determine an estimate for the probability of this distribution
    # by binning the particles into n discrete bins and then averaging
    # the particles in the mode bin.
    def __bestEstimateHelper__(self, particles):
        hist = [0]*20
        sums = [0.0]*20
        for p in particles:
            i = min(19, int(p*20))
            hist[i] += 1
            sums[i] += p
        maxCount = max(hist)
        for i in range(20):
            if(hist[i]==maxCount):
                return sums[i] / hist[i]




