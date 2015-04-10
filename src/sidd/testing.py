'''
Created on Apr 9, 2015

@author: sub253
'''
from pattern.text import parsetree, Chunk, pprint, parse
sent = 'the mobile web is more important than mobile apps.'
#sent ='There are two more scripts of interest.'
s = parsetree(sent, tokenize = True, relations=True, lemmata = True)
#chunk = Chunk(s)
# 

#parse(sent, relations=True))
print s
chunkList=[chunk.type for sentence in s for chunk in sentence.chunks]
relationList=[rel for sentence in s for rel in sentence.relations]

print chunkList
print relationList
#print chunk.subject

if 'VP' in chunkList and 'SBJ' in relationList:
    print 'exists'
    
import rake
rake_object = rake.Rake('../takahe/resources/stopwords.en.dat', 1, 3, 1)
keywords = rake_object.run(sent)
sequence = ' '.join(w for w, t in keywords)
print sequence
print "Keywords:", keywords