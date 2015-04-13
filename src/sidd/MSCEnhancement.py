'''
Created on Apr 9, 2015

@author: sub253
'''
import ppdbMSC
from nltk.tag.stanford import POSTagger
import rake
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/xmlrpc',)

# Create server
server = SimpleXMLRPCServer(("localhost", 8000),
                            requestHandler=RequestHandler)
server.register_introspection_functions()


sentences_without_tags=['The outbreak is the largest ever reported in North America.',
'Enterovirus D68 caused outbreak of respiratory disease.',
'Clusters of the outbreak in the United States were reported in August.',
'The Midwest has been hit in this outbreak']

english_postagger = POSTagger('../../jars/english-left3words-distsim.tagger','../../jars/stanford-postagger.jar', encoding='utf-8')

#topic = '2014 Enterovirus D68 outbreak'
#introsentence = 'In August 2014, Enterovirus D68 caused clusters of respiratory disease in the United States.'
rake_object = rake.Rake('../takahe/resources/stopwords.en.dat', 1, 3, 1)
#keywords = rake_object.run(introsentence)
#sequence = ' '.join(w for w, t in keywords)
#query = topic + ' ' + sequence.strip()


def generateQuery(introsentence, stubtitle):
    keywords = rake_object.run(introsentence)
    sequence = ' '.join(w for w, t in keywords)
    query = stubtitle + ' ' + sequence.strip()
    print 'Query -- ', query
    return query
server.register_function(generateQuery, 'createQuery')


def setQuery(queryPython):
    return queryPython
server.register_function(setQuery, 'setQuery')

sentList=['Nasha is 2013 Indian adolescent comingofage film directed by Amit Saxena .',
'Stunning Sheetal Singh enjoyed the role as Tia , girlfriend of Saahil Shivam Patil .',
'The ambitious project directed by South superstar Aditya Om will have her in a pivotal role .',
'She is a critically acclaimed for her roles in Paanch and Nasha .']


def returnSummary(x, query):
    print 'Found query:', query
    #raw_sent_list=[]
    raw_sent_list=x
    #print type(sentences_without_tags)
    #for i in sentences_without_tags:
        #print i
        #raw_sent_list.append(i)
    scoredList, cosineMatrix = ppdbMSC.getSortedSentenceList(query, raw_sent_list, english_postagger, max_sentences=200)
    if len(raw_sent_list)<=4:
        max_length=1
    else:
        max_length=5    
    solutionList = ppdbMSC.generateSummary(scoredList, cosineMatrix, max_length)        
    summary = ' '.join(sent[0].upper() + sent [1:] for score, sent, i in solutionList)  
    if summary is None:
        #print type(summary)  
        return ' '
    else:
        return summary
server.register_function(returnSummary, 'summarize')

#print 'Final generated summary ==>', summary

#print returnSummary(sentList, 'Sheetal Singh sheetal singh indian television film actress born november 22')


server.serve_forever()