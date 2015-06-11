#!/usr/bin/python
import sys

title1 = 'id\ttitle\ttagnames\tauthor_id\tbody\tnode_type\tparent_id\tabs_parent_id\tadded_at\tscore\tstate_string\tlast_edited_id\tlast_activity_by_id\tlast_activity_at\tactive_revision_id\textra\textra_ref_id\textra_count\tmarked\n'
title2 = '\"id\"\t\"title\"\t\"tagnames\"\t\"author_id\"\t\"body\"\t\"node_type\"\t\"parent_id\"\t\"abs_parent_id\"\t\"added_at\"\t\"score\"\t\"state_string\"\t\"last_edited_id\"\t\"last_activity_by_id\"\t\"last_activity_at\"\t\"active_revision_id\"\t\"extra\"\t\"extra_ref_id\"\t\"extra_count\"\t\"marked\"\n'
currLine = None

def getVelue(str_):
    if str_.startswith("\"") and str_.endswith("\""):
        return str_[1:-1]
    else:
        return str_
        
def mapTo(line):
    items = line.replace("\n"," ").split("\t")
    if len(items) == 19:
        nodeId = getVelue(items[0])
        parentId =  getVelue(items[7])
        node_type = getVelue(items[5])
        body = getVelue(items[4])
        
        if node_type == "question":
            print "{0}\t{1}\t{2}".format(nodeId, len(body), node_type)
        elif node_type == "answer":
            print "{0}\t{1}\t{2}".format(parentId, len(body), node_type)
            
for line in sys.stdin:
    if line == title1 or line == title2:
        continue
            
    items = line.split("\t")
    if len(items) > 4 and getVelue(items[0]).isdigit() and getVelue(items[3]).isdigit():
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