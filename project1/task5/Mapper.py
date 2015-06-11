#!/usr/bin/python
import sys

title1 = 'id\ttitle\ttagnames\tauthor_id\tbody\tnode_type\tparent_id\tabs_parent_id\tadded_at\tscore\tstate_string\tlast_edited_id\tlast_activity_by_id\tlast_activity_at\tactive_revision_id\textra\textra_ref_id\textra_count\tmarked\n'
title2 = '\"id\"\t\"title\"\t\"tagnames\"\t\"author_id\"\t\"body\"\t\"node_type\"\t\"parent_id\"\t\"abs_parent_id\"\t\"added_at\"\t\"score\"\t\"state_string\"\t\"last_edited_id\"\t\"last_activity_by_id\"\t\"last_activity_at\"\t\"active_revision_id\"\t\"extra\"\t\"extra_ref_id\"\t\"extra_count\"\t\"marked\"\n'

def getValue(str_):
    if str_.startswith("\"") and str_.endswith("\""):
        return str_[1:-1]
    else:
        return str_

def mapTo(line):
    stuInfo = line.replace("\n"," ").split("\t")
    if len(stuInfo) == 19:
        nodeId = getValue(stuInfo[0])
        parentId = getValue(stuInfo[7])
        authorID = getValue(stuInfo[3])
        nodeType = getValue(stuInfo[5])
        if nodeType in ["question", "answer", "comment"]:
            if nodeType == "question":
                print "{0}\t{1}".format(nodeId, authorID)
            elif nodeType == "answer":
                print "{0}\t{1}".format(parentId, authorID)
            elif nodeType =="comment":
                print "{0}\t{1}".format(parentId, authorID)

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