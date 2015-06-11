#! /usr/bin/python

import sys

lineNum = 0

titleInfo = ["id","title","tagnames","author_id","body","node_type",
				"parent_id","abs_parent_id","added_at","score","state_string",
				"last_edited_id","last_activity_by_id","last_activity_at",
				"active_revision_id","extra","extra_ref_id","extra_count","marked"]
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
	
	if stuInfo[4][0] == '\"' and stuInfo[4][-1] == '\"':
		body = stuInfo[4][1 : -1]
	else:
		body = stuInfo[4]

	print "{0}".format(len(body))

