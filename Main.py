import sys
import signal
from WebRenderer import WebRenderer
from WikiData import WikiData

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

class WikiGame:
	def __init__(self):
		self.app = QApplication(sys.argv)
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		self.wr = WebRenderer()
		self.wikidb = WikiData()


	def show(self):
		w = QWidget()
		w.resize(250, 150)
		w.move(300, 300)
		w.setWindowTitle('Simple')
		w.show()

		self.page = QWebPage()
		self.view = QWebView()
		self.view.setPage(self.page)
		self.window = QMainWindow()
		self.window.setCentralWidget(self.view)

		mf = self.page.mainFrame()
		mf.load(QUrl("google.com"))
		self.window.show()
		sys.exit(self.app.exec_())

if __name__ == '__main__':
	game = WikiGame()
	game.show()
