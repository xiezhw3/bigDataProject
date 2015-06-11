#! /usr/bin/python

import sys
from BloomFilter import *

lineNum = 0

titleInfo = ["id","title","tagnames","author_id","body","node_type",
				"parent_id","abs_parent_id","added_at","score","state_string",
				"last_edited_id","last_activity_by_id","last_activity_at",
				"active_revision_id","extra","extra_ref_id","extra_count","marked"]

flag = True
bf = BloomFilter(500000, 7)
lines = open("../data/forum_users.tsv").read().splitlines()
for line in lines:
	if flag:
		flag = False
		continue

	userInfo = line.strip().split("\t")
	if userInfo[0][0] == '\"' and userInfo[0][-1] == '\"':
		userId = userInfo[0][1 : -1]
	else:
		userId = userInfo[0]

	if userInfo[1][0] == '\"' and userInfo[1][-1] == '\"':
		reputation = userInfo[1][1 : -1]
	else:
		reputation = userInfo[1]
	if int(reputation) > 10:
		bf.add(userId)

flag = True
while True:
	lineNum += 1
	line = sys.stdin.readline()
	if not line:
		break

	# Whether the line is the title line of the file
	if flag:
		notTitle = False
		for item in titleInfo:
			if line.find(item) == -1:
				notTitle = True

		if notTitle == False:
			flag = False
			continue

	stuInfo = line.strip().split("\t")
	while len(stuInfo) < 19:
		lineTemp = sys.stdin.readline()
		if not lineTemp:
			break
		line = line.strip() + lineTemp
		stuInfo = line.strip().split("\t")
	
	if stuInfo[3][0] == '\"' and stuInfo[3][-1] == '\"':
		autoId = stuInfo[3][1 : -1]
	else:
		autoId = stuInfo[3]

	if stuInfo[4][0] == '\"' and stuInfo[4][-1] == '\"':
		body = stuInfo[4][1 : -1]
	else:
		body = stuInfo[4]

	if bf.lookup(autoId):
		print "{0}\t{1}".format(autoId, len(body))

