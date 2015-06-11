# coding: utf-8

import re

class HTML_Tool:
	def __init__(self):
		#非贪婪模式匹配 \t, \n, 空格, 超链接, 图片
		self.BegCharToNoneRex = re.compile(r'\t|\n| |<a.*?>|<img.*>|<span.*?>')
		#非贪婪模式匹配任意标签
		self.endCharToNoneRex = re.compile(r'<.*?>')

		#用非贪婪模式匹配任意<p>标签
		self.BgnPartRex = re.compile(r'<p.*?>')
		self.CharToNextLine = re.compile(r'<br/>|<br />|</p>|</div>|<tr>|</tr>')
		self.CharToNextTab = re.compile(r'<td.*?>')

		self.SimbolToSpace = re.compile(r',|=|-|/|:|;|!|\\|\"|\?|\'\'|\+|\[|\]|\.|\(|\)|\*|\/|_|#')

		self.NumToSpace = re.compile(r'\s+[0-9]+\s+')  # 匹配单纯数字

		#将一些html符号转为原始符号
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