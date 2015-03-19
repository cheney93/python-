# coding: utf-8

import urllib2
import re


class QSBK:
	def __init__(self):
		self.pageIndex = 1
		self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
		self.headers = {'User-Agent': self.user_agent}
		self.stories = []
		self.enable = False

	def getPage(self, pageIndex):
		try:
			url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
			request = urllib2.Request(url, headers=self.headers)
			response = urllib2.urlopen(request)
			pageCode = response.read().decode('utf-8')
			return pageCode
		except urllib2.URLError, e:
			if hasattr(e, 'reason'):
				print e.reason
				return None

	def getPageItems(self, pageIndex):
		pageCode = self.getPage(pageIndex)
		if not pageCode:
			print u'页面没有数据!'
			return None
		pattern = re.compile(
			'<div.*?class="author.*?">.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class' +
			'="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',
			re.S
		)
		items = re.findall(pattern, pageCode)
		pageStories = []
		for item in items:
			haveImg = re.search('img', item[3])
			if not haveImg:
				pageStories.append([item[0].strip(), item[1].strip(), item[2].strip(), item[4].strip()])
		return pageStories

	def loadPage(self):
		if self.enable == True:
			if len(self.stories) < 2:
				pageStories = self.getPageItems(self.pageIndex)
				if pageStories:
					self.stories.append(pageStories)
					self.pageIndex += 1

	def getOneStory(self, pageStories, page):
		for story in pageStories:
			Input = raw_input()
			self.loadPage()
			if Input == 'Q':
				self.enable = False
				return
			print u"第%d页\t发布人:%s\t发布时间:%s\n%s\n赞:%s\n" % (page, story[0], story[1], story[2], story[3])

	def start(self):
		print u'欢迎阅读热门段子!按回车阅读下一条，按"Q"退出'
		self.enable = True
		self.loadPage()
		nowPage = 0
		while self.enable:
			if len(self.stories) > 0:
				pageStories = self.stories[0]
				nowPage += 1
				self.getOneStory(pageStories, nowPage)
				del self.stories[0]


if __name__ == '__main__':
	dch = QSBK()
	dch.start()
