'''
Created on Mar 30, 2015

@author: sub253
'''
#!/usr/bin/python

# Copyright 2014, Gurobi Optimization, Inc.

# This example formulates and solves the following simple MIP model:
#  maximize
#        x +   y + 2 z
#  subject to
#        x + 2 y + 3 z <= 4
#        x +   y       >= 1
#  x, y, z binary

from gurobipy import *


##create the optimization model from the transformation object list

def maxWindowEstimator(indices, transObjectList):
    maxIndex=0
    for transObject in transObjectList:
        set1=set(indices)
        set2=transObject.indices
        commonElem=set1.intersection(set2)
        if not commonElem:
            continue
        else:
            max_s1=max(set1)
            max_s2=max(set2)
            if max(max_s1, max_s2) > maxIndex:
                maxIndex=max(max_s1, max_s2)
    return maxIndex  


def formLMSequence(wordObjectList,transObject, indices,transObjectList, window_size=2):
    #sequence=''
    r_window_size=2
    min_index=min(indices)
    diff=min_index-window_size
    while(diff<0):
            window_size=window_size - 1
            diff=min_index-window_size
    start_index=min(diff, min_index)
    listWords=wordObjectList[start_index:min_index]
    sequence = ' '.join(v.token for v in listWords)
    maxIndex=maxWindowEstimator(indices, transObjectList)
    nextWords=[]
    if maxIndex == 0:
        nextWords=wordObjectList[max(indices)+1:max(indices)+1+r_window_size]
    else:
        nextWords=wordObjectList[max(indices)+1:maxIndex+r_window_size]
    #nextWords=wordObjectList[max(indices)+1:]
    forwardSequence = ' '.join(v.token for v in nextWords)
    sequence=sequence.strip()+' '+transObject.targetSequence+' '+forwardSequence
    return sequence
#     if min_index - 1 >= 0 and min_index-2 >=0:
#         sequence = wordObjectList[min_index-2].token.lower()+' '+ wordObjectList[min_index-1].token.lower()+' '+transObject.targetSequence
#         return sequence.strip()
#     elif min_index - 1 >= 0:
#         sequence = wordObjectList[min_index-1].token.lower()+' '+transObject.targetSequence
#         return sequence.strip()
#     else:
#         sequence=transObject.targetSequence
#         return sequence.strip()

def formNoChangeSequence(wordObjectList,transObject, min_index,window_size=4):
    #sequence=''
    diff=min_index-window_size
    while(diff<=0):
            window_size=window_size - 1
            diff=min_index-window_size
    start_index=min(diff, min_index)
    listWords=wordObjectList[start_index:min_index]
    sequence = ' '.join(v.token for v in listWords)
    sequence=sequence.strip()+' '+transObject.sourceSequence
    return sequence
      
            
def simpleWordComponent(targetSequence, wordFrequency):
    simpleScore=0.0
    total=0.0
    for word in targetSequence.split():
        if word in wordFrequency:
            simpleScore +=wordFrequency[word]
            total +=1
    if total > 0.0:
        return simpleScore/total
    else:
        return 1


def solveILP(transObjectList, wordObjectList, lm, wordFrequency, favorCompression=False, favorSimpleWords=True):
    try:

    # Create a new model
        m = Model("mip1")

    # Create variables
        #i=0
        varlist=[]
        for i in xrange(len(transObjectList)):
            #i=i+1
            varlist.append(m.addVar(vtype=GRB.BINARY, name="var_"+str(i)))
            #y = m.addVar(vtype=GRB.BINARY, name="y")
            #z = m.addVar(vtype=GRB.BINARY, name="z")
        # Integrate new variables
        m.update()
    
        #print m.getVarByName()
        # Set objective
        objFunction = LinExpr()
        for transObject in transObjectList:
            #print 'FB Prob =>', transObject.forwardProb, transObject.backwardProb
            #coeff1=(float(transObject.forwardProb) * float(transObject.backwardProb)) 
            paraphraseSequence = formLMSequence(wordObjectList,transObject, transObject.indices, transObjectList)
            tokenDiff=len(transObject.targetSequence.split()) - len(transObject.sourceSequence.split())
            print transObject.sourceSequence,'=>', transObject.targetSequence 
            print 'Sequence-->',paraphraseSequence
            lmNormalizer = 1.0
            if len(paraphraseSequence.split())>=3:
                lmNormalizer= len(paraphraseSequence.split()) - 2
            else:
                lmNormalizer = 1.0
            #coeff2=1.0/(1.0-(lm.score(paraphraseSequence)/lmNormalizer))
            coeff2=1.0/(1.0-(lm.score(paraphraseSequence)))
            simpleWordScorerTarget=simpleWordComponent(transObject.targetSequence,wordFrequency)
            simpleWordScorerSource=simpleWordComponent(transObject.targetSequence,wordFrequency)
            if simpleWordScorerTarget>=simpleWordScorerSource:
                simpleWordScorer=max(simpleWordScorerTarget,simpleWordScorerSource)/min(simpleWordScorerTarget,simpleWordScorerSource)
            else:
                simpleWordScorer=1.0   
            #coeff2=1.0*len(transObject.sourceSequence.split())*len(transObject.targetSequence.split())/(1.0 - lm.score(paraphraseSequence))
            if tokenDiff<0 and favorCompression is True:
                coeff2 = 1+coeff2
            if favorSimpleWords is True:
                coeff2=coeff2*simpleWordScorer
            print 'Sequence-->',paraphraseSequence, coeff2    
            #coeff=2*coeff1*coeff2/(coeff1+coeff2) 
            coeff=coeff2
            #print coeff1, coeff2
            #coeff=coeff2
            #if len(transObject.targetSequence.split()) > 1:
                #coeff=coeff*len(transObject.targetSequence.split()) 
            var=m.getVarByName("var_"+str(transObjectList.index(transObject)))  
            objFunction.add(coeff*var)
            #print 'Type of objfunction',type(objFunction)
        
        #print objFunction
        m.setObjective(objFunction, GRB.MAXIMIZE)

        #print m.getObjective()
        # Add constraint: x + 2 y + 3 z <= 4
        #m.addConstr(x + 2 * y + 3 * z <= 4, "c0")

        # Add constraint: x + y >= 1
        #m.addConstr(x + y >= 1, "c1")
        for transObject0 in transObjectList:
            for transObject1 in transObjectList:
                if transObjectList.index(transObject0) == transObjectList.index(transObject1):
                    continue
                indices0=transObject0.indices
                indices1=transObject1.indices
                if set(indices0).intersection(set(indices1)):
                    #print 'Indices 0 -->'+ str(indices0) + ', Indices 1 -->'+ str(indices1)
                    #print transObject0.sourceSequence+"==>"+transObject0.targetSequence
                    #print transObject1.sourceSequence+"==>"+transObject1.targetSequence
                    var0=m.getVarByName("var_"+str(transObjectList.index(transObject0)))  
                    var1=m.getVarByName("var_"+str(transObjectList.index(transObject1)))
                    #print var0.varName+'=='+var1.varName
                    #if not var0.varName == var1.varName:
                    m.addConstr(var0 + var1, GRB.LESS_EQUAL, 1.0, "constraint_"+var0.varName+"_"+var1.varName) 
                    
        #m.update()
        
        #print m.getConstrs()
        m.update()
        #print m.getConstrs()
        m.optimize()

        finalTransformationList=[]
        #varList=[m.getVars()]
        #print varList
        i=0
        for v in m.getVars():
            if v.x == 1.0:
                finalTransformationList.append(transObjectList[i])
            i=i+1    
            #print('%s %g' % (v.varName, v.x))

        #print('Obj: %g' % m.objVal)
        
        #print 'Final operations:',len(finalTransformationList)
        
        #for to in finalTransformationList:
            #print to.sourceSequence
        m.discardConcurrentEnvs()
    except GurobiError:
        print('Error reported')
    return finalTransformationList    
#solveILP([1,2,3])        
        