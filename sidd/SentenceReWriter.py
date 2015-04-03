# encoding:utf-8
'''

Created on Mar 31, 2015

@author: sub253
'''
###START IMPORTS####
import os
from sidd.MSA.Paraphraser import *
from sidd.MSA import PPDBLoader
from nltk.corpus import stopwords
from nltk.tag.stanford import POSTagger
import nltk
import codecs
import logging
import random
from pynlpl.lm.lm import ARPALanguageModel

#####ENF OF IMPORT####

MAX_NGRAMS=5
os.environ['STANFORD_PARSER'] = '../jars/'
os.environ['STANFORD_MODELS'] = '../jars/'
os.environ['JAVA_HOME'] ='C:/jdk1.7.0_07/bin'  ##HP Laptop
#os.environ['JAVA_HOME'] = 'C:/Program Files/Java/jdk1.7.0_17/bin' ##Lab desktop
#pp_type='noccg' #lexical, phrasal, noccg
#file_size='s'
stopwordList=stopwords.words('english')
#ppdbFileName='ppdb-1.0-'+file_size+'-'+pp_type+'.gz'
ppdbDir='../ppdb'
posFilterList=['NNP','NNPS'] ## DO NOT MODIFY words with these tags

#lm = LM('../jars/lm_csr_5k_vp_2gram.arpa')
rawFileCorpus='../dataset-sentences/treatment-sentences-tokenized-stanford.txt'

logging.basicConfig(level=logging.INFO)
logging.info("Starting program")
#lm = ARPALanguageModel('../jars/lm_giga_20k_nvp_3gram.arpa', mode='trie' )
lm = ARPALanguageModel('../jars/lm_csr_5k_vp_2gram.arpa')
logging.info("Loaded Language model....")
LexicalPPDict=PPDBLoader.createLexParaphraseMap('l', 'lexical',ppdbDir )
logging.info("Loaded lexical paraphrases....")
PhrasalPPDict=PPDBLoader.createGeneralParaphraseMap('s',ppdbDir) ## Name is coded in PpdbLoader class
logging.info("Loaded phrasal, one to many and many to one paraphrases....")
wordFrequency=PPDBLoader.createWordFreqMap(rawFileCorpus, stopwordList)
#== Uncomment this if running single sentence ==#

english_postagger = POSTagger('../jars/english-left3words-distsim.tagger','../jars/stanford-postagger.jar', encoding='utf-8')
readfile = codecs.open('../dataset-sentences/treatment-sentences-tokenized-stanford.txt',encoding='utf-8', errors='ignore')
writefile=codecs.open('../dataset-sentences/rewritten.txt','w','utf-8',errors='ignore')
i=0
for line in readfile:
    randNum = random.choice([1,2])
#     if randNum == 1:
#         continue
    if i==10:
        break
    #i +=1
    #if i<=374:
        #continue
    sentence = line.strip()
    print sentence
    #sentence = 'In most cases, 3-M syndrome is diagnosed shortly after birth, based upon a thorough clinical evaluation, identification of characteristic physical findings (e.g., low birth weight, short stature, characteristic craniofacial and skeletal malformations, etc.), and/or a variety of specialized tests, such as advanced imaging techniques.'

    #sentence=unicode(sentence,'utf-8')
    print 'Original Sentence:', sentence
    #sentence='An Emirates and an Etihad aircraft, flying in opposite directions came in proximity of each other over the Indian Ocean, leading to a collision alert warning in the two cockpits on Sunday night.'
    #orig_Sentence=sentence.decode('utf-8', errors='replace')
    orig_Sentence=sentence
    sentence = english_postagger.tag(nltk.word_tokenize(sentence))
    print sentence[0][0]
    print sentence
    modSentence = sentenceTuple(sentence)
    
    ppCandidateList=generateNGramCandidatesToChange(modSentence, MAX_NGRAMS=4)
    all_possible_transformations=generateListOfPossibleTransformations(ppCandidateList,
                                                                        LexicalPPDict=LexicalPPDict,
                                                                        PhrasalPPDict=PhrasalPPDict,
                                                                        stopwords=stopwordList, 
                                                                        useIdentities=False)

    rewrittenSentence=ILPSolverToSentence(all_possible_transformations, modSentence, lm, wordFrequency)
    print 'Original Sentence:', orig_Sentence
    print 'Final Generated:', rewrittenSentence
    writefile.write('Orig:'+orig_Sentence + '\n')
    writefile.write('PP:'+rewrittenSentence +'\n')
    writefile.write('===========================\n')
    i=i+1
  
writefile.close()
#== Uncomment this if running single sentence ==#

# sentence='In most cases, 3-M syndrome is diagnosed shortly after birth, based upon a thorough clinical evaluation, identification of characteristic physical findings (e.g., low birth weight, short stature, characteristic craniofacial and skeletal malformations, etc.), and/or a variety of specialized tests, such as advanced imaging techniques.'
# orig_Sentence=sentence
# #english_postagger = POSTagger('../jars/english-left3words-distsim.tagger','../jars/stanford-postagger.jar')
# sentence = english_postagger.tag(nltk.word_tokenize(sentence))
#  
# ppCandidateList=pp.generateNGramCandidatesToChange(sentence,MAX_NGRAMS=8)
# all_possible_transformations=pp.generateListOfPossibleTransformations(ppCandidateList, 
#                                                                    LexicalPPDict=LexicalPPDict, PhrasalPPDict=PhrasalPPDict,
#                                                                    stopwords=stopwordList,
#                                                                    useIdentities=False)
# rewrittenSentence=pp.ILPSolverToSentence(all_possible_transformations, sentence, lm)
# print 'Original Sentence:', orig_Sentence
# print 'Final Generated:', rewrittenSentence