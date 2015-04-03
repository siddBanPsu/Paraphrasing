'''
Created on 28-Mar-2015

@author: siddban
'''
from sidd.MSA import Optimizer
'''
Created on Mar 27, 2015

@author: sub253
'''
###START IMPORTS####
from PPDBLoader import LexWord, Phrase
from nltk.util import OrderedDict
from nltk.util import ngrams
from sidd.MSA.NGrams import Operator,TransformationObject, CandidateObject, WordObject
####END IMPORTS#####

#MAX_NGRAMS=5
# os.environ['STANFORD_PARSER'] = '../../jars/'
# os.environ['STANFORD_MODELS'] = '../../jars/'
# os.environ['JAVA_HOME'] = 'C:/Program Files/Java/jdk1.7.0_17/bin'
# #pp_type='noccg' #lexical, phrasal, noccg
# #file_size='s'
#stopwordList=stopwords.words('english')
# #ppdbFileName='ppdb-1.0-'+file_size+'-'+pp_type+'.gz'
# 
delim='_'
posFilterList=['NNP','NNPS']
# 
# LexicalPPDict=PPDBLoader.createLexParaphraseMap('l', 'lexical')
# PhrasalPPDict=PPDBLoader.createGeneralParaphraseMap('s', 'phrasal')

# for l, pp in LexicalPPDict.iteritems():
#     if(l.word == 'matter'):
#         print l.word+"/"+l.ccg+"==>"
#         for k in pp:
#             print k.word+"/"+k.forwardProb+","+k.backwardProb

#sentence='The Fokker aircraft was on a routine training flight when it came down near the airstrip.'
# sentence='His research contributions have been primarily in the fields of information extraction, information integration and information visualization.'
# english_postagger = POSTagger('../../jars/wsj-0-18-left3words-distsim.tagger','../../jars/stanford-postagger.jar')
# sentence = english_postagger.tag(nltk.word_tokenize(sentence))
def sentenceTuple(sentence):
    modSentence = []
    position=0
    for w,t in sentence:
        if t not in ('NNP', 'NNPS') and position == 0:
            modSentence.append((w.lower(),t))
        else:
            modSentence.append((w,t))    
        position +=1    
    #print modSentence
    return modSentence




def generateNGramCandidatesToChange(sentence,MAX_NGRAMS):
    final_Sentence=''
    token_position=0
    for w,t in sentence:
        #if t not in ('NNP', 'NNPS') and token_position == 0:
            #final_Sentence=final_Sentence + ' ' + w.lower() + delim + t + delim + str(token_position)
        
        final_Sentence=final_Sentence + ' ' + w + delim + t + delim + str(token_position)    
        token_position=token_position+1
    print final_Sentence.strip()
    candidates=OrderedDict()
    n = [i+1 for i in xrange(MAX_NGRAMS)]
    for i in n:
        #print i
        nGrams = ngrams(final_Sentence.strip().split(), i)
        candidates[i]=list(nGrams)
 
    #total_candidates_to_change=sum(len(v) for v in candidates.itervalues())
    #print 'Total candidates that can be changed ~~ ',total_candidates_to_change

    paraphraseCandidateList=[]
    for i in n:  
        ngramlist=candidates[i]
        for ngram in ngramlist:
            #print ngrams
            candidateObject=CandidateObject(ngram,i)
            paraphraseCandidateList.append(candidateObject)
            #print candidateObject.wordObjectList[0].token
            #  sequence=' '.join(gram.split('/')[0] for gram in ngrams)
            #indices=[int(gram.split('/')[2]) for gram in ngrams]
            #print sequence, indices
            
    return paraphraseCandidateList
    #print 'Total candidates that can be changed ~~ ',len(paraphraseCandidateList)  



def generateListOfPossibleTransformations(paraphraseCandidateList,LexicalPPDict,PhrasalPPDict, stopwords, useIdentities=False):
    list_of_possible_transformations=[]
    for candidate in paraphraseCandidateList:
        unwantedElements=set(candidate.posList).intersection(set(posFilterList))
        if candidate.countGrams == 1  and candidate.sequence.lower().strip() not in stopwords and len(unwantedElements)==0:
            lexWordKey=LexWord(candidate.sequence.strip().lower(), candidate.posSequence.strip())
            if LexicalPPDict.has_key(lexWordKey):
                pp = LexicalPPDict.get(lexWordKey)
            #print candidate.sequence+'==>'
                for k in pp:
                #print k.word
                    transObject=TransformationObject(candidate.sequence.strip(),k.word, candidate.indices, k.forwardProb, k.backwardProb)
                    list_of_possible_transformations.append(transObject)
                #print k.word+'_'+lexWordKey.ccg+'=='+k.forwardProb+","+k.backwardProb
    ##First check lexical paraphrases possible
    
    for candidate in paraphraseCandidateList:
        unwantedElements=set(candidate.posList).intersection(set(posFilterList))
        #print '2',candidate.posSequence.strip(), 'unwanted', str(unwantedElements)
        if candidate.countGrams is not 1 and len(unwantedElements)==0:
            lexWordKey=Phrase(candidate.sequence.strip().lower(), candidate.posSequence.strip())
            if PhrasalPPDict.has_key(lexWordKey):
                pp = PhrasalPPDict.get(lexWordKey)
            #print candidate.sequence+'==>'
                for k in pp:
                #print k.word+'_'+lexWordKey.ccg+'=='+k.forwardProb+","+k.backwardProb    
                    transObject=TransformationObject(candidate.sequence.strip(),k.word, candidate.indices, k.forwardProb, k.backwardProb)
                    list_of_possible_transformations.append(transObject)
    
    
    #Identical changes
    if useIdentities is True:
        for candidate in paraphraseCandidateList:
            unwantedElements=set(candidate.posList).intersection(set(posFilterList))
            #print '2',candidate.posSequence.strip(), 'unwanted', str(unwantedElements)
            if candidate.countGrams is not 1 and len(unwantedElements)==0:
                transObject=TransformationObject(candidate.sequence.strip(),candidate.sequence.strip(), candidate.indices, '0.01', '0.01')
                list_of_possible_transformations.append(transObject)
            if candidate.countGrams == 1  and candidate.sequence.lower().strip() not in stopwords and len(unwantedElements)==0:    
                transObject=TransformationObject(candidate.sequence.strip(),candidate.sequence.strip(), candidate.indices, '0.01', '0.01')
                list_of_possible_transformations.append(transObject)
                
    return list_of_possible_transformations

def upcase_first_letter(s):
    return s[0].upper() + s[1:]


def createWordObjectList(tagged_sentence):
    wordObjectList=[]
    i=0
    for w, t in tagged_sentence:
        wR=w+delim+t+delim+str(i)
        wordObject=WordObject(wR)
        wordObjectList.append(wordObject)
        i=i+1
    return wordObjectList    


def ILPSolverToSentence(list_of_possible_transformations, tagged_sentence, lm,wordFrequency):            
    #list_of_possible_transformations=generateListOfPossibleTransformations(paraphraseCandidateList)
    print 'List of possible transformations....'

    for i, tobject in enumerate(list_of_possible_transformations):
        print i,":",tobject.sourceSequence,'==>',tobject.targetSequence+'/'+str(tobject.indices)
        
    wordObjectList=createWordObjectList(tagged_sentence)
    #for wordObject in wordObjectList:
        #print 'Word object', wordObject.token
    final_selected_transformations=Optimizer.solveILP(list_of_possible_transformations, wordObjectList, lm, wordFrequency)

    operations=[]
    for transformationObject in final_selected_transformations:
        tokens = transformationObject.sourceSequence.split()
        indices = transformationObject.indices
        sequenceToChange=''
        k=0
        for token in tokens:
            sequenceToChange=sequenceToChange+' '+token+'_'+str(indices[k])
            sequenceToChange = sequenceToChange.strip()
            k=k+1
        operations.append(Operator(sequenceToChange,transformationObject.targetSequence))   
    #transformationObject.sourceSequence, transformationObject.indices, transformationObject.targetSequence
    
    ## Modify original sentence
    list_of_indices_to_change=[]
    for transformationObject in final_selected_transformations:
        for element in transformationObject.indices:
            list_of_indices_to_change.append(element)

    #print list_of_indices_to_change

    token_position=0
    sentence_positions=''
    for w,t in tagged_sentence:
        if token_position in list_of_indices_to_change:
            sentence_positions=sentence_positions+w+'_'+str(token_position)+' '
        else:
            sentence_positions=sentence_positions+w+' '         
        token_position=token_position+1

    #sentence_positions=sentence_positions.strip()    

    for operation in operations:
        #print '$$Operations$$', sentence_positions, '||', operation.sourceSequence, '||', operation.targetSequence
        sentence_positions=sentence_positions.replace(operation.sourceSequence+' ', operation.targetSequence+' ')

    return upcase_first_letter(sentence_positions.strip())
   
#print 'Final sentence:',  upcase_first_letter(sentence_positions.strip())