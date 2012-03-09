import sys
import signal

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

DEBUG=True
'''Currently, you should do:
wr = WebRenderer()
wr.render("URL")
--Wait until wr.loading == False
wr.image should contain the image you need.

'''
class WebRenderer:
	def loadHandler(self, result):
		self.page.setViewportSize(self.page.mainFrame().contentsSize())
		self.image = QImage(self.page.viewportSize() + QSize(10,10), QImage.Format_ARGB32)
		painter = QPainter(self.image)
		self.page.mainFrame().render(painter)
		painter.end()
		self.loading = False

	def __init__(self):
		self.page = QWebPage()
		self.view = QWebView()
		self.view.setPage(self.page)
		self.window = QMainWindow()
		self.window.setCentralWidget(self.view)
		self.page.connect(self.page, SIGNAL("loadFinished(bool)"), self.loadHandler)
		self.image = None
		
	def render(self, url):
		self.loading = True

		mf = self.page.mainFrame()
		mf.load(QUrl(url))
