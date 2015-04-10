'''
Created on Mar 13, 2015

@author: sub253
'''
import nltk
from textblob import TextBlob
from _elementtree import parse
text = """The Buddha, the Godhead, resides quite as comfortably in the circuits of a digital
computer or the gears of a cycle transmission as he does at the top of a mountain
or in the petals of a flower. To think otherwise is to demean the Buddha...which is
to demean oneself."""
 
# Used when tokenizing words
sentence_re = r'''(?x)      # set flag to allow verbose regexps
      ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
    | \w+(-\w+)*            # words with optional internal hyphens
    | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
    | \.\.\.                # ellipsis
    | [][.,;"'?():-_`]      # these are separate tokens
'''
 
lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()
 
#Taken from Su Nam Kim Paper...
grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        
    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
"""
chunker = nltk.RegexpParser(grammar)
 
toks = nltk.regexp_tokenize(text, sentence_re)
postoks = nltk.tag.pos_tag(toks)
 
print postoks
 
tree = chunker.parse(postoks)
 
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
 
 
def leaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label=='NP'):
        yield subtree.leaves()
 
def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    word = stemmer.stem_word(word)
    word = lemmatizer.lemmatize(word)
    return word
 
def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword."""
    accepted = bool(2 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted
 
 
def get_terms(tree):
    for leaf in leaves(tree):
        term = [ normalise(w) for w,t in leaf if acceptable_word(w) ]
        yield term
 
terms = get_terms(tree)
 
for term in terms:
    for word in term:
        print word,
    print
    
    
wiki = TextBlob("A number of methods have been recommended to help ease symptoms, including adequate liquid intake and rest")    
print wiki.noun_phrases

###########EXAMPLE###########

from nltk.tree import *


# Tree manipulation

# Extract phrases from a parsed (chunked) tree
# Phrase = tag for the string phrase (sub-tree) to extract
# Returns: List of deep copies;  Recursive
def ExtractPhrases( myTree, phrase):
    myPhrases = []
    if (myTree.label == phrase):
        myPhrases.append( myTree.copy(True) )
    for child in myTree:
        if (type(child) is Tree):
            list_of_phrases = ExtractPhrases(child, phrase)
            if (len(list_of_phrases) > 0):
                myPhrases.extend(list_of_phrases)

#return myPhrases

test = Tree.fromstring('(ROOT(S (SBAR (IN If) (S (NP (NN radiofrequency) (NN catheter) (NN ablation)) (VP (VBZ is) (ADVP (RB successfully)) (VP (VBN performed))))) (, ,) (NP (DT the) (NN condition)) (VP (VBZ is) (ADVP (RB generally)) (VP (VBN considered) (S (VP (VBN cured))))) (. .)))')
print "Input tree: ", test

test.pprint()
# print "\nNoun phrases:"
# list_of_noun_phrases = ExtractPhrases(test, 'NP')
# for phrase in list_of_noun_phrases:
#     print " ", phrase


# GUI
# for sentence in sentences:
#     sentence.draw()