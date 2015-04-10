'''
Created on Mar 25, 2015

@author: sub253
'''
# import wikipedia
# currentpage = wikipedia.page("ChemXSeer")
# 
# print currentpage.title
# print currentpage.categories
# print currentpage.sections
from nltk.tag.stanford import POSTagger
from sidd.paraphraser.Paraphraser import *
import nltk
import os
# lm=ARPALanguageModel('../../jars/lm_csr_5k_vp_2gram.arpa',encoding='utf-8')
# 
# print lm.score('Hello how are you')
os.environ['JAVA_HOME'] = 'C:/Program Files/Java/jdk1.7.0_17/bin' ##Lab desktop
from sidd.paraphraser import PPDBLoader
english_postagger = POSTagger('../../jars/english-left3words-distsim.tagger','../../jars/stanford-postagger.jar', encoding='utf-8')
syntacticMap=PPDBLoader.createSyntacticParaphraseMap('s', '../../ppdb')

    #sentence='An Emirates and an Etihad aircraft, flying in opposite directions came in proximity of each other over the Indian Ocean, leading to a collision alert warning in the two cockpits on Sunday night.'
    #orig_Sentence=sentence.decode('utf-8', errors='replace')
sentence = 'The box is thrown.'    
orig_Sentence=sentence
sentence = english_postagger.tag(nltk.word_tokenize(sentence))
print sentence[0][0]
print sentence
modSentence = sentenceTuple(sentence)
    
ppCandidateList=generateNGramCandidatesToChange(modSentence, MAX_NGRAMS=4)
#all_possible_transformations=generateListOfPossibleTransformations(ppCandidateList,
#                                                                        LexicalPPDict=LexicalPPDict,
#                                                                        PhrasalPPDict=PhrasalPPDict,
#                                                                        stopwords=stopwordList, 
#                                                                        useIdentities=False)
