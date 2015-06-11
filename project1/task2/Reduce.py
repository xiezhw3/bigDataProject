#!/usr/bin/python
import sys
 
oldKey = None
answers = []
question = None

def output():
    if len(answers) == 0:
        avg = 0
    else:
        avg = sum(answers) / float(len(answers))
    print oldKey, question, avg

 
for line in sys.stdin:
    dataMapped = line.strip().split("\t")
    if len(dataMapped) != 3:
        continue
 
    nodeId, bodyLen, nodeType = dataMapped
    if oldKey and oldKey != nodeId:
        output()
        answers = []
        question = None
 
    oldKey = nodeId
    if nodeType=="question":
        question = int(bodyLen)
    elif nodeType=="answer":
        answers.append(int(bodyLen))
 
if oldKey != None:
    output()