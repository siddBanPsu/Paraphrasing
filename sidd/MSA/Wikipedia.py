'''
Created on Mar 25, 2015

@author: sub253
'''
# import wikipedia
# currentpage = wikipedia.page("ChemXSeer")
# 
# print currentpage.title
# print currentpage.categories
# print currentpage.sections
from pynlpl.lm.lm import ARPALanguageModel
lm=ARPALanguageModel('../../jars/lm_csr_5k_vp_2gram.arpa',encoding='utf-8')

print lm.score('Hello how are you')