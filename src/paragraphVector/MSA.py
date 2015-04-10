#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Mar 11, 2015

@author: sub253
'''
from nltk import sent_tokenize
import codecs
from django.utils.encoding import smart_str, smart_unicode

input_file='../inputFile/treatment-sentences.txt'

def readSentencesOfSection(input_file):
    wikiSentences=[]
    with codecs.open(input_file,'r',encoding='utf-8', errors='ignore') as f:
        for line in f:
            line=line.strip()
            sentences=sent_tokenize(unicode(line))
            for sentence in sentences:
            #sentence=sentence.decode('utf-8')
                wikiSentences.append(sentence)
    return wikiSentences

def getParseTrees(sentenceList):
    for sentence in sentenceList:
        print sentence

sentenceList=readSentencesOfSection(input_file)

f_Write=codecs.open('treatment-sentence-tokenized.txt','w','utf-8')
for sentences in sentenceList:
    f_Write.write(sentences+'\n')
    
f_Write.close()
getParseTrees(sentenceList)





print len(sentenceList)