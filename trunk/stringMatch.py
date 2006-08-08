#! /usr/bin/env python


class stringMatch:


    def __init__(self):
        print 'stringMatch'


    
    # Return True if individual words match
    def __getWordMatch__(self, a,b):
        if((a=='') | (b=='')):
            return False
        na = a.lower()
        nb = b.lower()
        return self.__prefixMatch__(na, nb)
    #return (na == nb)


    #return a numerical score for how well the user's input matches the definition
    def getStringMatch(self, w1, w2):
        #This should decide how close the two words are to each other.
        w1s = [a.strip() for a in w1.split(',')]
        w2s = [a.strip() for a in w2.split(',')]
        for a in w1s:
            for b in w2s:
                if(self.__getWordMatch__(a,b)):
                    return 1
        return 0

    def __prefixMatch__(self, w1, w2):
        c = self.__getLongestPrefix__(w1, w2)
        if((c == len(w1)) | (c==len(w2))):
            return True
        elif(c >= 4):
            return True
        elif((2*c >= len(w1)) | (2*c >= len(w2))):
            return True
        else:
            return False


    def __getLongestPrefix__(self, w1, w2):
        count = 0
        try:
            while(w1[count]==w2[count]):
                count += 1
        except:
            count -= 1
        return count+1


