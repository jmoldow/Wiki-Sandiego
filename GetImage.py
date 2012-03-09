import sys
import signal

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

class ImageGrabber:
	def __init__(self):
		app = QApplication(sys.argv)
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		self.page = QWebPage()
		self.view = QWebView()
		self.view.setPage(self.page)
		self.window = QMainWindow()
		self.window.setCentralWidget(self.view)
		self.page.connect(self.page, SIGNAL("loadFinished(bool)"), self.loadHandler)
		
	def render(self, url):
		self.loading = True


		mf = self.page.mainFrame()
		u = QUrl(url)
		mf.load(u)

		while self.loading:
			while QApplication.hasPendingEvents():
				QCoreApplication.processEvents()

		image = QImage(self.page.viewportSize(), QImage.Format_ARGB32)
		painter = QPainter(image)
		mf.render(painter)
		painter.end()

		return image

	def loadHandler(self, result):
		self.loading = False

i = ImageGrabber()
i.render("http://web.mit.edu/dvorak42/www/")


import sys
import signal

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

def loadHandler(result):
	global loading
	loading = False

app = QApplication([])
page = QWebPage()
page.connect(page, SIGNAL("loadFinished(bool)"), loadHandler)

def load(url):
	page.mainFrame().load(QUrl(url))

def paint():
page.setViewportSize(page.mainFrame().contentsSize())
	image = QImage(page.viewportSize(), QImage.Format_ARGB32)
	painter = QPainter(image)
	page.currentFrame().render(painter)
	painter.end()
	return image


generateURL("google.com").save("TTT.png")
