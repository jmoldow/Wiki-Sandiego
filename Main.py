import sys
import signal
import WebRenderer
import WikiData

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

class WikiGame:
	def __init__(self):
		self.app = QApplication(sys.argv)
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		self.webrender = WebRenderer()
		self.wikidb = WikiData()

if __name__ == '__main__':
	game = WikiGame()
