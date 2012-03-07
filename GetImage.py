from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

class ImageGrabber:
	def __init__(self):
		app = QApplication([])
		self.page = QWebPage()
		self.view = QWebView()
		self.view.setPage(self.page)
		self.window = QMainWindow()
		self.window.setCentralWidget(self.view)
		self.page.connect(self.page, SIGNAL("loadFinished(bool)"), self.loadHandler)

	def render(self, url):
		self.loading = True

		self.page.mainFrame().load(QUrl(url))

		while self.loading:
			while QApplication.hasPendingEvents():
				QCoreApplication.processEvents()

		image = QImage(self.page.viewportSize(), QImage.Format_ARGB32)
		painter = QPainter(image)
		self.page.mainFrame().render(painter)
		painter.end()

		return image

	def loadHandler(self, result):
		self.loading = False

