'''
Created on Apr 9, 2015

@author: sub253
'''
from pattern.text import parsetree, Chunk, pprint, parse
sent = 'A number of methods have been recommended to help ease symptoms, including adequate liquid intake and rest.'
#sent ='There are two more scripts of interest.'
s = parsetree(sent, tokenize = True, relations=True, lemmata = True)
#chunk = Chunk(s)
# 

#parse(sent, relations=True))
print s
relationList=s.sentences[0].relations

print 'Relationlist=>',relationList
sbjstring=''
objstring=''
if 'SBJ' in relationList:
    for chunk in relationList['SBJ'].values():
        print chunk.words
        sbjstring =sbjstring+' '+ ' '.join(word.string for word in chunk.words)
        
if 'OBJ' in relationList:
    for chunk in relationList['OBJ'].values():
        print chunk.words
        objstring =objstring+' '+ ' '.join(word.string for word in chunk.words)
print sbjstring.strip()
print objstring.strip()
#print chunk.subject

    
# import rake
# rake_object = rake.Rake('../takahe/resources/stopwords.en.dat', 1, 3, 1)
# keywords = rake_object.run(sent)
# sequence = ' '.join(w for w, t in keywords)
# print sequence
# print "Keywords:", keywords