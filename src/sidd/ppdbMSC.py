'''
Created on Apr 4, 2015

@author: sub253
'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

# print sys.path
# print os.path.join(os.path.dirname(__file__), '..')
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
###START IMPORTS####
import os,sys
from takahe import takahe 
from nltk.corpus import stopwords
from sidd.paraphraser.Paraphraser import *
import nltk
import logging
import cPickle as pickle
import datetime
import networkx as nx
import igraph
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer, \
    TfidfVectorizer
from random import shuffle
from sklearn.metrics.pairwise import linear_kernel
from gurobipy import *
from pynlpl.lm.lm import ARPALanguageModel
from pattern.text import parsetree 
#####ENF OF IMPORT####


MAX_NGRAMS=5
os.environ['STANFORD_PARSER'] = '../jars/'
os.environ['STANFORD_MODELS'] = '../jars/'

################################################################################
os.environ['JAVA_HOME'] = 'C:/Program Files/Java/jdk1.7.0_17/bin' ##Lab desktop
#pp_type='noccg' #lexical, phrasal, noccg
file_size='s'
stopwordList=stopwords.words('english')
#ppdbFileName='ppdb-1.0-'+file_size+'-'+pp_type+'.gz'
ppdbDir='../../ppdb/'
posFilterList=['NNP','NNPS'] ## DO NOT MODIFY words with these tags

logging.basicConfig(level=logging.INFO)
logging.info("Starting program")
lm = ARPALanguageModel('../../jars/lm_giga_20k_nvp_3gram.arpa', mode='trie')
#lm = ARPALanguageModel('../jars/lm_csr_5k_vp_2gram.arpa', mode='trie')
#lm = ARPALanguageModel('../../jars/lm_csr_5k_vp_2gram.arpa')
#rawFileCorpus='../../dataset-sentences/treatment-sentences-tokenized-stanford.txt'


#lm = ARPALanguageModel('../jars/lm_giga_20k_nvp_3gram.arpa', mode='trie' )
#lm = ARPALanguageModel('../jars/lm_giga_20k_nvp_3gram.arpa' )
#lm = ARPALanguageModel('../jars/lm_csr_5k_vp_2gram.arpa', mode ='trie')
#lm = ARPALanguageModel('../jars/lm_csr_5k_vp_2gram.arpa')
logging.info("Loaded Language model....")
#LexicalPPDict=PPDBLoader.createLexParaphraseMap('s', 'lexical',ppdbDir )
# def save_object(obj, filename):
#     with open(filename, 'wb') as output:
#         pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

#save_object(LexicalPPDict, '../ppdb/s-lexical.pk1')
LexicalPPDict = pickle.load( open( ppdbDir+file_size+"-lexical.pk1", "rb" ) )
#print LexicalPPDict

logging.info("Loaded lexical paraphrases....")
a = datetime.datetime.now()
#PhrasalPPDict=PPDBLoader.createGeneralParaphraseMap('s',ppdbDir) ## Name is coded in PpdbLoader class
PhrasalPPDict=pickle.load( open( ppdbDir+file_size+"-phrasal.pk1", "rb" ) )
b = datetime.datetime.now()
logging.info("Loaded phrasal, one to many and many to one paraphrases....")
print(b - a)
#save_object(PhrasalPPDict, '../ppdb/s-phrasal.pk1')

#wordFrequency=PPDBLoader.createWordFreqMap(rawFileCorpus, stopwordList)

sentences = ["The/DT wife/NN of/IN a/DT former/JJ U.S./NNP president/NN \
Bill/NNP Clinton/NNP Hillary/NNP Clinton/NNP visited/VBD China/NNP last/JJ \
Monday/NNP ./PUNCT", "Hillary/NNP Clinton/NNP wanted/VBD to/TO visit/VB China/NNP \
last/JJ month/NN but/CC postponed/VBD her/PRP$ plans/NNS till/IN Monday/NNP \
last/JJ week/NN ./PUNCT", "Hillary/NNP Clinton/NNP paid/VBD a/DT visit/NN to/TO \
the/DT People/NNP Republic/NNP of/IN China/NNP on/IN Monday/NNP ./PUNCT", 
"Last/JJ week/NN the/DT Secretary/NNP of/IN State/NNP Ms./NNP Clinton/NNP \
visited/VBD Chinese/JJ officials/NNS ./PUNCT"]

def generateEnhancedSentences(sentences_no_tags, tagger):
    final_Sentences=[]
    for sentence_no_tag in sentences_no_tags:
        sentence_no_tag = tagger.tag(nltk.word_tokenize(sentence_no_tag))
        modifiedsentence = sentenceTuple(sentence_no_tag)
        #print '$', modifiedsentence
        ppCandidateList=generateNGramCandidatesToChange(modifiedsentence, MAX_NGRAMS=5)
        all_possible_transformations=generateListOfPossibleTransformations(ppCandidateList,
                                                                        LexicalPPDict=LexicalPPDict,
                                                                        PhrasalPPDict=PhrasalPPDict,
                                                                        stopwords=stopwordList, 
                                                                        useIdentities=False)

        #print 'Number of transformations:', len(all_possible_transformations)
        if len(all_possible_transformations) == 0:
            token_position=0
            sentence_positions=''
            for w,t in modifiedsentence:
                sentence_positions=sentence_positions+w+' '
                token_position=token_position+1
            final_Sentences.append(sentence_positions)
            return final_Sentences
        for transformationObject in all_possible_transformations:
            tokens = transformationObject.sourceSequence.split()
            indices = transformationObject.indices
            sequenceToChange=''
            
            k=0
            for token in tokens:
                #print indices[k]
                sequenceToChange=sequenceToChange+' '+token+'_'+str(indices[k])
                sequenceToChange = sequenceToChange.strip()
                k=k+1
                
            #Store info of which indices to change
            list_of_indices_to_change=[]
            for element in transformationObject.indices:
                list_of_indices_to_change.append(element)  
        
            #For REGEX, only modify the indices that require changing
            token_position=0
            sentence_positions=''
            for w,t in modifiedsentence:
                if token_position in list_of_indices_to_change:
                    sentence_positions=sentence_positions+w+'_'+str(token_position)+' '
                else:
                    sentence_positions=sentence_positions+w+' '         
                token_position=token_position+1
        
            operation= Operator(sequenceToChange,transformationObject.targetSequence)
            sentence_positions=sentence_positions.replace(operation.sourceSequence+' ', operation.targetSequence+' ')    
            #print '#',sentence_positions
            final_Sentences.append(sentence_positions)
    return final_Sentences 


def generateTempRewrittenSentences(taggedSentences):
    final_tagged_Sentences=[]
    for ensent in taggedSentences:
        tagged_sentence=''
        for w, t in ensent:
            tagged_sentence=tagged_sentence+w+'/'+t+' '
        final_tagged_Sentences.append(tagged_sentence.strip())
    return final_tagged_Sentences


# sentences_without_tags=[]
# for sentence in sentences:
#     #print sentence
#     sentence_without_tag=''
#     for tokens in sentence.split():
#         word=  tokens.split('/')[0]
#         sentence_without_tag=sentence_without_tag+' '+word
#     sentences_without_tags.append(sentence_without_tag.strip())        
# 
# print 'Just sentences==>'
# print sentences_without_tags


# print len(sentences)




def scipy_to_igraph(matrix, nodelist,  directed=True):
    sources, targets = matrix.nonzero()
    #weights = matrix[sources, targets]
    names=[val+'|'+str(c) for val, c in nodelist]
    return igraph.Graph(zip(sources, targets), directed=directed, vertex_attrs={'name':names})


def generateMultiplePaths(taggedSentences):
    compresser = takahe.word_graph(taggedSentences, \
                                nb_words = 10, \
                                lang = 'en', \
                                punct_tag = "." )

    matrix=nx.to_scipy_sparse_matrix(compresser.graph)
    nodelist=compresser.graph.nodes()
    g= scipy_to_igraph(matrix,nodelist)
    return g


def getVertex(graph, string):
    for vertex in graph.vs:
        if string in vertex['name']: 
            return vertex

def adjlist_find_paths(a, n, m, path=[]):
    "Find paths from node index n to m using adjacency list a."
    path = path + [n]
    if n == m:
        return [path]
    paths = []
    for child in a[n]:
        if child not in path:
            child_paths = adjlist_find_paths(a, child, m, path)
            for child_path in child_paths:
                paths.append(child_path)
                if(len(paths)==10000):
                    return paths
    return paths

def paths_from_to(graph, source, dest):
    "Find paths in graph from vertex source to vertex dest."
    a = graph.get_adjlist()
    n = source.index
    m = dest.index
    return adjlist_find_paths(a, n, m)        

def getWordFromVertexName(nameString):
    word=nameString.split('/')[0]
    if word not in ['-start-','-end-']:
        return word
    else:
        return ''


def getSortedSentenceList(query, raw_sentence_list, english_postagger, min_words=14, max_sentences=2000):
# igraph object
    enhancedSentences=generateEnhancedSentences(raw_sentence_list,english_postagger)
    print 'Enhanced sentences==>', len(enhancedSentences)
    taggedSentences=english_postagger.tag_sents(nltk.word_tokenize(sent) for sent in enhancedSentences)
    taggedSentences=generateTempRewrittenSentences(taggedSentences)
    iobject = generateMultiplePaths(taggedSentences)
    startvertex = getVertex(iobject, '-start-/-/-start-')
    endvertex = getVertex(iobject, '-end-/-/-end-')
    vertexList = iobject.vs()
    allpaths = paths_from_to(iobject, startvertex, endvertex)
    shuffle(allpaths)
    allpaths=allpaths[0:2000]
    generatedSentences = []
    a = datetime.datetime.now()
    print 'starting paths...'
    sentence_container = {}
    for path in allpaths:
        paired_parentheses = 0
        quotation_mark_number = 0
        if len(path) >= min_words: 
            sentence = ' '.join(getWordFromVertexName(vertexList[element]['name']) for element in path) 
            for word in sentence.split():
                if word == '(':
                    paired_parentheses -= 1
                elif word == ')':
                    paired_parentheses += 1
                elif word == '"' or word == '\'\'' or word == '``':
                    quotation_mark_number += 1
            if paired_parentheses == 0 and \
                (quotation_mark_number%2) == 0 and \
                not sentence_container.has_key(sentence.strip()):   
                generatedSentences.append(sentence.strip())  
                sentence_container[sentence.strip()]=1
            
    
    b = datetime.datetime.now()
    print 'done with paths' , (b-a)
    shuffle(generatedSentences)
    generatedSentences=generatedSentences[0:max_sentences]
    for gensent in generatedSentences:
        s = parsetree(gensent, tokenize = True, relations=True, lemmata = True)
        chunkList=[chunk.type for row in s for chunk in row.chunks]
        relationList=[rel for row in s for rel in row.relations]
        if 'VP' not in chunkList or 'SBJ' not in relationList: #subject verb
            generatedSentences.remove(gensent)
            
    #shuffle(generatedSentences)        
    
    
    docs=[]
    docs.append(query) ## Query add
    docs.extend(generatedSentences)
       
    bow_matrix = TfidfVectorizer(stop_words=stopwordList).fit_transform(docs)
    normalized = TfidfTransformer().fit_transform(bow_matrix)
    
    cosine_similarity_matrix = (normalized[1:] * normalized[1:].T).A
    sources, targets = cosine_similarity_matrix.nonzero()
    similarity_igraph = igraph.Graph(zip(sources, targets), directed=True)
    scores = igraph.Graph.pagerank(similarity_igraph)
    
    docqueryRelevance = linear_kernel(normalized[0:1], normalized[1:]).flatten()
    
    scoredList = [(scores[i] * docqueryRelevance[i], s, i) for i, s in enumerate(generatedSentences)]
    #scoredList = [(docqueryRelevance[i], s, i) for i, s in enumerate(generatedSentences)]
    
    #for score, sent, i in scoredList:
        #print score, sent, i
    #cosine_similarity_matrix=np.asmatrix(cosine_similarity_matrix)    
    return scoredList, cosine_similarity_matrix    


# for i in xrange(len(generatedSentences)):
#     cossimlist = linear_kernel(normalized[i:i+1], normalized)
    #print cossimlist

 
def generateSummary(all_path_list, cosineMatrix, maxlength, languageModel=lm): 
    try:
    # Create a new model
        m = Model("mip2")
        varlist=[]
        for score, sent, i in all_path_list:
            varlist.append(m.addVar(vtype=GRB.BINARY, name="var_"+str(i)))
        m.update()
        objFunction = LinExpr()
        for score, sent, i in all_path_list:
            lmNormalizer=len(sent.split())
            #lm_score=-(lm.score(sent))
            lm_score=lmNormalizer*1.0/(1.0-(lm.score(sent)))
            var=m.getVarByName("var_"+str(i))
            objFunction.add(score*lm_score*var)
        m.setObjective(objFunction, GRB.MAXIMIZE) 
        
        m.update()
        
        #print m.getObjective()
        #Redundancy constraint
        #redundancyConstraint= LinExpr()
        for score, sent, i in all_path_list:
            a=cosineMatrix[i,:]
            indices= np.where(a>0.1) #redundancy value
            var=m.getVarByName("var_"+str(i))
            for k in indices[0]:
                if k == i:
                    continue
                simvar=m.getVarByName("var_"+str(k))
                m.addConstr(var + simvar, GRB.LESS_EQUAL, 1.0, "constraint_"+var.varName+"_"+simvar.varName) 
                
         
        m.update()
        
        #print m.getConstrs()
        
        lengthConstraint=LinExpr()
        for score, sent, i in all_path_list:
            var=m.getVarByName("var_"+str(i))
            lengthConstraint.add(var)
        
        m.addConstr(lengthConstraint, GRB.LESS_EQUAL, maxlength, "length")
        m.optimize()
         
        solutionList=[] 
        i=0
        for v in m.getVars():
            if v.x == 1.0:
                print all_path_list[i]
                solutionList.append(all_path_list[i])
            i=i+1
        m.discardConcurrentEnvs()
        return solutionList
    except GurobiError:
        print('Error reported') 
    return   

