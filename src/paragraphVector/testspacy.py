'''
Created on Mar 12, 2015

@author: sub253
'''
from __future__ import unicode_literals # If Python 2
from spacy.en import English
from spacy import *
from numpy import dot
from numpy.linalg import norm
nlp = English()
tokens = nlp(u'I ate the pizza with anchovies.', tag=True, parse=True)
pizza = tokens[5]
#print pizza.repvec

cosine = lambda v1, v2: dot(v1, v2) / (norm(v1) * norm(v2))
words = [w for w in nlp.vocab if w.has_repvec]
words.sort(key=lambda w: cosine(w.repvec, pizza.repvec))
words.reverse()

print('1-20', ', '.join(w.orth_ for w in words[0:20]))