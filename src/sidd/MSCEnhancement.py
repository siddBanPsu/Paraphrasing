'''
Created on Apr 9, 2015

@author: sub253
'''
import ppdbMSC
from nltk.tag.stanford import POSTagger
import rake

sentences_without_tags=['The outbreak is the largest ever reported in North America.',
'Enterovirus D68 caused outbreak of respiratory disease.',
'Clusters of the outbreak in the United States were reported in August.',
'The Midwest has been hit in this outbreak']

english_postagger = POSTagger('../../jars/english-left3words-distsim.tagger','../../jars/stanford-postagger.jar', encoding='utf-8')

topic = '2014 Enterovirus D68 outbreak'
introsentence = 'In August 2014, Enterovirus D68 caused clusters of respiratory disease in the United States.'
rake_object = rake.Rake('../takahe/resources/stopwords.en.dat', 1, 3, 1)
keywords = rake_object.run(introsentence)
sequence = ' '.join(w for w, t in keywords)
query = topic + ' ' + sequence.strip()
print 'Query', query
scoredList, cosineMatrix = ppdbMSC.getSortedSentenceList(query, sentences_without_tags, english_postagger, max_sentences=500)
solutionList = ppdbMSC.generateSummary(scoredList, cosineMatrix)        
summary = ' '.join(sent[0].upper() + sent [1:] for score, sent, i in solutionList)
print 'Final generated summary ==>', summary