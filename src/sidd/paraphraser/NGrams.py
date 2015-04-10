'''
Created on Mar 29, 2015

@author: sub253
'''
delim='_'

class WordObject(object):
    def __init__(self, gram):
        self.token=gram.split(delim)[0]
        self.posTag=gram.split(delim)[1]
        self.index=gram.split(delim)[2]

class CandidateObject(object):
    def __init__(self, grams, countGrams):
        self.countGrams=countGrams
        self.grams=grams
        self.sequence=' '.join(gram.split(delim)[0] for gram in grams)
        self.posSequence=' '.join(gram.split(delim)[1] for gram in grams)
        self.posList=[gram.split(delim)[1] for gram in grams]
        self.indices=[int(gram.split(delim)[2]) for gram in grams]
        self.wordObjectList=[WordObject(gram) for gram in grams]


class TransformationObject(object):
    def __init__(self, sourceSequence, targetSequence, sourceIndices,forwardProb,backwardProb):
        self.sourceSequence=sourceSequence
        self.indices=sourceIndices
        self.targetSequence=targetSequence
        self.forwardProb=forwardProb
        self.backwardProb=backwardProb
    def __hash__(self):
        return hash(self.sourceSequence, self.targetSequence, self.indices, self.forwardProb)
    def __eq__(self, other):
        return (self.sourceSequence, self.targetSequence, self.indices, self.forwardProb) == (other.sourceSequence, other.targetSequence, other.indices, other.forwardProb)    
        

class Operator(object):
    def __init__(self, sourceSequence, targetSequence):
        self.sourceSequence=sourceSequence
        self.targetSequence=targetSequence
