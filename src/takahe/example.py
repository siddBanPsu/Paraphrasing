#!/usr/bin/python
# -*- coding: utf-8 -*-

from resources import takahe_old
from nltk import word_tokenize, pos_tag
import codecs
################################################################################
sentences = ["The/DT wife/NN of/IN a/DT former/JJ U.S./NNP president/NN \
Bill/NNP Clinton/NNP Hillary/NNP Clinton/NNP visited/VBD China/NNP last/JJ \
Monday/NNP ./PUNCT", "Hillary/NNP Clinton/NNP wanted/VBD to/TO visit/VB China/NNP \
last/JJ month/NN but/CC postponed/VBD her/PRP$ plans/NNS till/IN Monday/NNP \
last/JJ week/NN ./PUNCT", "Hillary/NNP Clinton/NNP paid/VBD a/DT visit/NN to/TO \
the/DT People/NNP Republic/NNP of/IN China/NNP on/IN Monday/NNP ./PUNCT", 
"Last/JJ week/NN the/DT Secretary/NNP of/IN State/NNP Ms./NNP Clinton/NNP \
visited/VBD Chinese/JJ officials/NNS ./PUNCT"]
################################################################################

# Create a word graph from the set of sentences with parameters :
# - minimal number of words in the compression : 6
# - language of the input sentences : en (english)
# - POS tag for punctuation marks : PUNCT
sentences=[]
with codecs.open('test.txt', 'r',  'utf-8') as f:
	for line in f:
		line = line.replace('%%:','')
		text = word_tokenize(line.strip())
		tagged=pos_tag(text)
		sentence =''
		for word, token in tagged:
			sentence=sentence + word+'/'+token+' '
		sentences.append(sentence.strip())
			
compresser = takahe_old.word_graph( sentences, 
							    nb_words = 6, 
	                            lang = 'en', 
	                            punct_tag = "." )

# Get the 50 best paths
candidates = compresser.get_compression(50)

# 1. Rerank compressions by path length (Filippova's method)
for cummulative_score, path in candidates:

	# Normalize path score by path length
	normalized_score = cummulative_score / len(path)

	# Print normalized score and compression
	print round(normalized_score, 3), ' '.join([u[0] for u in path])

# Write the word graph in the dot format
compresser.write_dot('test.dot')

print '*********************'
# 2. Rerank compressions by keyphrases (Boudin and Morin's method)
reranker = takahe_old.keyphrase_reranker( sentences,  
									  candidates, 
									  lang = 'en' )

reranked_candidates = reranker.rerank_nbest_compressions()

# Loop over the best reranked candidates
for score, path in reranked_candidates:
	
	# Print the best reranked candidates
	print round(score, 3), ' '.join([u[0] for u in path])