#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html


"""

"""
from itertools import izip
import logging
import sys
import os
from word2vec import Word2Vec, Sent2Vec, LineSentence
import codecs


logging.basicConfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.info("running %s" % " ".join(sys.argv))


category='Diseases_and_disorders'

logging.basicConfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.info("running %s" % " ".join(sys.argv))

#input_file = 'test2.txt'
input_file = '../inputFile/'+category+'.corpus.txt' 
model = Word2Vec(LineSentence(input_file), size=50, window=7, sg=0, min_count=3, workers=8)
model.save(input_file + '.model')
model.save_word2vec_format(input_file + '.vec')

# f_wv=codecs.open('../inputFile/word-vec.txt','w','utf-8')
# with open('../inputFile/vocab.txt') as textfile1, open('../inputFile/wordVectors.txt') as textfile2: 
#         for x, y in izip(textfile1, textfile2):
#             x = x.strip()
#             y = y.strip()
#             f_wv.write(x+'\t'+y+'\n')
# f_wv.close()

sent_file = input_file
model = Sent2Vec(LineSentence(sent_file), model_file=input_file + '.model')
model.save_sent2vec_format(sent_file + '.vec')

program = os.path.basename(sys.argv[0])
logging.info("finished running %s" % program)