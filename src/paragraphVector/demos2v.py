#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""

"""

import logging
import sys
import os
import re
import csv
import codecs
from word2vec import Word2Vec, Sent2Vec, LineSentence
from nltk import word_tokenize,pos_tag, sent_tokenize

category='Diseases_and_disorders'

f_Write=codecs.open('../inputFile/'+category+'.corpus.pos.txt','w','utf-8')
with open('../inputFile/'+category+'.corpus.txt') as f:
    reader=csv.reader(f,delimiter='\t')
    for class_name,x,content in reader:
        #print content
        content= content.decode("utf8")
        sentencesList=sent_tokenize(content)
        out_str=''
        for sentence in sentencesList:
            sentence_tagged=pos_tag(word_tokenize(sentence))
            out_str = out_str + ' '+ ' '.join([word+"_"+tag for word,tag in sentence_tagged if re.search(r"^[a-z0-9]", word.lower())])
        f_Write.write(out_str+'\n')
f_Write.close()

logging.basicConfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.info("running %s" % " ".join(sys.argv))

#input_file = 'test2.txt'
input_file = '../inputFile/'+category+'.corpus.pos.txt' 
model = Word2Vec(LineSentence(input_file), size=300, window=5, sg=0, min_count=5, workers=8)
model.save(input_file + '.model')
model.save_word2vec_format(input_file + '.vec')


# f_Write=open('../inputFile/American_soft_drinks.corpus.pos.txt','w')
# with open("sent.txt") as f:
#     content = f.readlines()
#     for line in content:
#         sentencesList=sent_tokenize(line)
#         out_str=''
#         for sentence in sentencesList:
#             sentence_tagged=pos_tag(word_tokenize(sentence))
#             out_str = out_str+' '+' '.join([word+"_"+tag for word,tag in sentence_tagged])
#         f_Write.write(out_str+'\n')
# f_Write.close()



#sent_file = '../inputFile/American_soft_drinks.corpus.pos.txt'
sent_file=input_file
model = Sent2Vec(LineSentence(sent_file), model_file=input_file + '.model')
model.save_sent2vec_format(sent_file + '.s2v.vec')

program = os.path.basename(sys.argv[0])
logging.info("finished running %s" % program)


