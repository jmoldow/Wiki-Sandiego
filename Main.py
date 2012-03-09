import sys
import signal

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

class WikiGame:
	def __init__(self):
		self.app = QApplication(sys.argv)


if __name__ == '__main__':
	game = WikiGame()
