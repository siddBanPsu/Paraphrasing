'''
Created on Mar 29, 2015

@author: sub253
'''
import gzip
from collections import defaultdict
import re
import codecs

#DIR_PPDB = '../../ppdb'

class LexWord(object):
    def __init__(self, word, ccg):
        self.ccg = ccg
        self.word = word
    def __hash__(self):
        return hash((self.word, self.ccg))
    def __eq__(self, other):
        return (self.word, self.ccg) == (other.word, other.ccg)

class Phrase(object):
    def __init__(self, word, ccg):
        self.ccg = ccg
        self.word = word
    def __hash__(self):
        return hash(self.word)
    def __eq__(self, other):
        return (self.word) == (other.word)


class Paraphrase(object):
    def __init__(self, word, forwardProb, backwardProb):
        self.forwardProb = forwardProb
        self.backwardProb = backwardProb
        self.word = word
    def __hash__(self):
        return hash(self.word)
    def __eq__(self, other):
        return (self.word) == (other.word)



def createWordFreqMap(filename, stopwordList):
    fileToRead = codecs.open(filename, "r","utf-8", errors='replace')
    text = fileToRead.read()
    fileToRead.close()
    word_list = text.lower().split(None)
    word_freq = {}
    for word in word_list:
        if word not in stopwordList:
            word_freq[word] = word_freq.get(word, 0) + 1
    #keys = sorted(word_freq.keys())
    #for word in keys:
        #print "%-10s %d" % (word, word_freq[word])
    return word_freq    


def createLexParaphraseMap(file_size, pp_type, ppdbDir):     
    ppdbFileName = 'ppdb-1.0-' + file_size + '-' + pp_type + '.gz'   
    f = gzip.open(ppdbDir + '/' + ppdbFileName)
    d = defaultdict(list)
    for line in f:
        line = line.decode('utf-8')
        cols = line.split('|||')
        ccgTag = cols[0].replace("[", "").replace("]", "").strip()
        # print posTag
        wordForm = cols[1].strip()
        if re.match("[^a-zA-Z]", wordForm):  # does not start with word character
            continue
        if re.match("[^a-zA-Z]", cols[2].strip()):  # does not start with word character
            continue
        if len(wordForm) <3 or len(cols[2].strip()) <3:
            continue
        word = LexWord(wordForm, ccgTag)
        attributes = cols[3].strip()
        # print attributes
        matchObjs = re.search(r'p\(e\|f\)=(.*?) .* p\(f\|e\)=(.*?) ', attributes)
        if matchObjs is not None:
        # print "match:",matchObjs.group(1), matchObjs.group(2)
            paraPhrase = Paraphrase(cols[2].strip(), matchObjs.group(1), matchObjs.group(2))
        # print paraPhrase.word+"/"+paraPhrase.backwardProb
            d[word].append(paraPhrase)
    f.close()         
    return d     


def createGeneralParaphraseMap(file_size,ppdbDir): 
    pp_types=['phrasal','m2o','o2m'] 
    d = defaultdict(list)  
    for pp_type in pp_types:
        ppdbFileName = 'ppdb-1.0-' + file_size + '-' + pp_type + '.gz'   
        f = gzip.open(ppdbDir + '/' + ppdbFileName)
        for line in f:
            line = line.decode('utf-8')
            cols = line.split('|||')
            ccgTag = cols[0].replace("[", "").replace("]", "").strip()
            # print posTag
            wordForm = cols[1].strip()
            if re.match("[^a-zA-Z]", wordForm):  # does not start with word character
                continue
            if re.match("[^a-zA-Z]", cols[2].strip()):  # does not start with word character
                continue
            if len(wordForm) <3 or len(cols[2].strip()) <3:
                continue
            word = Phrase(wordForm, ccgTag)
            attributes = cols[3].strip()
            # print attributes
            matchObjs = re.search(r'p\(e\|f\)=(.*?) .* p\(f\|e\)=(.*?) ', attributes)
            if matchObjs is not None:
            # print "match:",matchObjs.group(1), matchObjs.group(2)
                paraPhrase = Paraphrase(cols[2].strip(), matchObjs.group(1), matchObjs.group(2))
                if paraPhrase not in d[word]:
                    # print paraPhrase.word+"/"+paraPhrase.backwardProb
                    d[word].append(paraPhrase)
        f.close() 
               
    return d       
    # print cols[0],cols[1],cols[2], cols[3]
