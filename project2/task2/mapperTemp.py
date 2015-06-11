#! /usr/bin/python

import sys
import re
class HTML_Tool:
    def __init__(self):
        self.BegCharToNoneRex = re.compile(r'\t|\n| |<a.*?>|<img.*>|<span.*?>')
        self.endCharToNoneRex = re.compile(r'<.*?>')
        self.BgnPartRex = re.compile(r'<p.*?>')
        self.CharToNextLine = re.compile(r'<br/>|<br />|</p>|</div>|<tr>|</tr>')
        self.CharToNextTab = re.compile(r'<td.*?>')
        self.SimbolToSpace = re.compile(r',|=|-|/|:|;|!|\\|\"|\?|\'\'|\+|\[|\]|\.|\(|\)|\*|\/|_|#')
        self.NumToSpace = re.compile(r'\s+[0-9]+\s+')
        self.replaceTab = [("&quot;","\""),("&amp;","&"),("&lt;","<"),("&gt;",">"),("&nbsp;"," "),("[\n]+","\n"),("[\t]+"," "),("[ ]+"," ")]
        
    def replace_char(self, str_):
        for i in self.replaceTab:
            str_ = str_.replace(i[0], i[1])
        str_ = self.BegCharToNoneRex.sub(" ", str_)
        str_ = self.BgnPartRex.sub(" ", str_)
        str_ = self.CharToNextLine.sub(" ", str_)
        str_ = self.CharToNextTab.sub(" ", str_)
        str_ = self.endCharToNoneRex.sub(" ", str_)
        str_ = self.SimbolToSpace.sub(" ", str_)
        str_ = self.NumToSpace.sub(" ", str_)
        return str_
        
def getNoTagStr(content):
    tool = HTML_Tool()
    content = tool.replace_char(content)
    return content
    
def getValue(str_):
    if len(str_) < 2:
        return str_
    if str_[0] == '\"' and str_[-1] == '\"':
        return str_[1 : -1]
    return str_
    
def getWord(str_):
    if str_[0] == '\"' and str_[-1] == '\"':
        return str_[1 : -1]
    if str_[0] == '\'' and str_[-1] == '\'':
        return str_[1 : -1]
    if str_[-1] == '\'' or str_[-1] == '\"':
        return str_[0 : -1]
    if str_[0] == '\'' or str_[0] == '\"':
        return str_[1 : len(str_)]
    return str_
    
notFound = ["the", "be", "to", "of", "and", "a", "in", "that", "have", "I", "it", "for",
            "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", "his", "by",
            "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one", "all",
            "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get",
            "which", "go", "me", "when", "make", "can", "like", "time", "no", "just", "him",
            "know", "take", "person", "into", "year", "your", "good", "some", "could", "them",
            "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think",
            "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", "way", "even",
            "new", "want", "because", "any", "these", "give", "day", "most", "us"]

isWord = re.compile(r'^[\w\'-]+$')
notWord = re.compile(r'^[^a-zA-Z]+$')

title1 = 'id\ttitle\ttagnames\tauthor_id\tbody\tnode_type\tparent_id\tabs_parent_id\tadded_at\tscore\tstate_string\tlast_edited_id  last_activity_by_id last_activity_at\tactive_revision_id\textra\textra_ref_id\textra_count marked\n'
title2 = '\"id\"\t\"title\"\t\"tagnames\"\t\"author_id\"\t\"body\"\t\"node_type\"\t\"parent_id\"\t\"abs_parent_id\"\t\"added_at\"\t\"score\"\t\"state_string\"\t\"last_edited_id  last_activity_by_id last_activity_at\"\t\"active_revision_id\"\t\"extra\"\t\"extra_ref_id\"\t\"extra_count marked\"\n'

def getValue(str_):
    if str_.startswith("\"") and str_.endswith("\""):
        return str_[1:-1]
    else:
        return str_

def mapTo(line):
    stuInfo = line.replace("\n"," ").split("\t")
    nodeId = getValue(stuInfo[0])
    node_type = getValue(stuInfo[5])
    parentId = getValue(stuInfo[6])
    body = getValue(stuInfo[4])
    if node_type != "question":
        nodeId = parentId
        
    words = set()
    wordList = getNoTagStr(body).split(" ")
    for i in range(0, len(wordList)):
        if wordList[i] == '':
            continue
            
        word = getWord(wordList[i])
        if (word not in words) and (word not in notFound) and (word != "")\
            and (word != " ") and isWord.match(word) and not notWord.match(word):
            print "{0}\t{1}".format(getWord(wordList[i]), nodeId + ":" + str(i))

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