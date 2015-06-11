#! /usr/bin/python

import sys
import re

title1 = 'id\ttitle\ttagnames\tauthor_id\tbody\tnode_type\tparent_id\tabs_parent_id\tadded_at\tscore\tstate_string\tlast_edited_id  last_activity_by_id last_activity_at\tactive_revision_id\textra\textra_ref_id\textra_count marked\n'
title2 = '\"id\"\t\"title\"\t\"tagnames\"\t\"author_id\"\t\"body\"\t\"node_type\"\t\"parent_id\"\t\"abs_parent_id\"\t\"added_at\"\t\"score\"\t\"state_string\"\t\"last_edited_id  last_activity_by_id last_activity_at\"\t\"active_revision_id\"\t\"extra\"\t\"extra_ref_id\"\t\"extra_count marked\"\n'

notFound = ["the", "be", "to", "of", "and", "a", "in", "that", "have", "I", "it", "for",
            "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", "his", "by",
            "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one", "all",
            "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get",
            "which", "go", "me", "when", "make", "can", "like", "time", "no", "just", "him",
            "know", "take", "person", "into", "year", "your", "good", "some", "could", "them",
            "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think",
            "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", "way", "even",
            "new", "want", "because", "any", "these", "give", "day", "most", "us"]

def getValue(str_):
    if str_.startswith("\"") and str_.endswith("\""):
        return str_[1:-1]
    else:
        return str_

def isWord(word):
    if ':' in word or '(' in word or ')' in word or '#' in word or '\"' in word \
        or '=' in word or '!' in word or word.startswith('\'') or word.startswith('\"') or word.endswith("\"") \
        or word.endswith("\'") or "<a" in word:
        return False
    return True


def mapTo(line):
    stuInfo = line.replace("\n", " ").split("\t")
    nodeId = getValue(stuInfo[0])
    node_type = getValue(stuInfo[5])
    parentId = getValue(stuInfo[6])
    body = getValue(stuInfo[4])
    if node_type != "question":
        nodeId = parentId

    wordList = getValue(body).split() 
    words = set()
    for i in range(0, len(wordList)):
        if wordList[i] == '':
            continue
        word = wordList[i].lower()
        if (word not in words) and (word not in notFound) and isWord(word):
            words.add(word)
            print "{0} {1}".format(word, nodeId + ":" + str(1 + body.find(wordList[i])))

flag = True
currLine = None
for line in sys.stdin:
    if line == title1 or line == title2:
        continue
            
    items = line.strip().split("\t")
    if len(items) > 4 and getValue(items[0]).isdigit() and getValue(items[3]).isdigit():
        if currLine != None:
            mapTo(currLine)
        currLine = line
    else:
        if currLine == None:
            currLine = line
        else:
            currLine += line
            
if currLine != None:
    mapTo(currLine)