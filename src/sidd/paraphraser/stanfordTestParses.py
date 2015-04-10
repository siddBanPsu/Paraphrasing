'''
Created on Mar 18, 2015

@author: sub253
'''
import os
from nltk.parse import stanford
from nltk.tree import Tree
import codecs
from unidecode import unidecode
os.environ['STANFORD_PARSER'] = '../../jars/'
os.environ['STANFORD_MODELS'] = '../../jars/'

# parser = stanford.StanfordParser(model_path="../../jars/englishPCFG.ser.gz")
# sentences = parser.raw_parse_sents(("Hello, My name is Melroy.", "What is your name?"))
# print Tree.fromstring(str(sentences[0]))
# print sentences[1]

f = codecs.open('../../dataset-sentences/treatment-sentences-trees-stanford.txt','r','utf-8',errors='replace')
for line in f:
    #if(line)
    line=line.strip()
    if line.startswith('(ROOT'):
        #continue        
        print Tree.fromstring(unidecode(line))
# print sentences[1]
        

    


