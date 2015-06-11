#! /usr/bin/python

import sys
import re

#title = ["id","title","tagnames","author_id","body","node_type",
#        "parent_id","abs_parent_id","added_at","score","state_string",
#        "last_edited_id","last_activity_by_id","last_activity_at",
#        "active_revision_id","extra","extra_ref_id","extra_count","marked"]

commonWord = ["the","be","to","of","and","a","in","that","have","I","it","for","not","on","with",
            "he","as","you","do","at","this","but","his","by","from","they","we","say","her","she",
            "or","an","will","myone","all","would","there","their","what","so","up","out","if",
            "about","who","get","which","go","me","when","make","can","like","time","no","just",
            "him","know","take","person","into","year","your","good","some","could","them","see",
            "other","than","then","now","look","only","come","its","over","think","also","back",
            "after","use","two","how","our","work","first","well","way","even","new","want","because",
            "any","these","give","day","most","us"]

newline = None

def dequote(t):
    if t.startswith("\"") and t.endswith("\""):
        return t[1:-1]
    else:
        return t

def output(newline):
    one = newline.replace("\n"," ").split("\t")
    if len(one) == 19:
        body = dequote(one[4])
        sid = dequote(one[0])
        pattern = re.compile('\d*|\w+')
        keyword = pattern.findall(body)
        count = 0
        for key in keyword:
            count += 1
            if key not in commonWord:
                print "{0}\t{1}\t{2}".format(key, sid, str(count))

for line in sys.stdin:
    one = line.split("\t")
    if len(one)>4 and dequote(one[0]).isdigit() and dequote(one[3]).isdigit():
        if newline != None:
            output(newline)
        newline = line
    else:
        if newline == None:
            newline = line
        else:
            newline += line

if newline != "":
    output(newline)