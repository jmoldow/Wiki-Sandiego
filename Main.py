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
		self.SCREEN_ORIGIN = QPoint(0, 0)   # the origin / top-left corner of the window
		self.SCREEN_SIZE = QSize(992, 672)  # the resolution for the entire window
		self.SCREEN_RECT = QRect(self.SCREEN_ORIGIN, self.SCREEN_SIZE)  # the QRect that represents the entire window
		self.MAIN_PANEL_SIZE = QSize(704, self.SCREEN_SIZE.height())	# the size of the main game panel
		self.MAIN_PANEL_RECT = QRect(self.SCREEN_ORIGIN, self.MAIN_PANEL_SIZE)  # the QRect that represents the main game panel
		self.SIDE_PANEL_ORIGIN = QPoint(self.MAIN_PANEL_SIZE.width(), 0)	# the origin / top-left corner of the notepad side panel
		self.SIDE_PANEL_SIZE = QSize(self.SCREEN_SIZE.width()-self.MAIN_PANEL_SIZE.width(), self.SCREEN_SIZE.height())  # the size of the notepad side panel
		self.SIDE_PANEL_RECT = QRect(self.SIDE_PANEL_ORIGIN, self.SIDE_PANEL_SIZE)  # the QRect that represents the notepad side panel

		# set up the window
		self.window = QWidget()
		self.window.setGeometry(self.SCREEN_RECT)
		self.window.setWindowTitle('Wiki Sandiego')

		# set up the notepad side panel
		self.side_panel = QTextEdit(QString(u'Your Detective Notepad<br /><br /><br />'), self.window)
		self.side_panel.setGeometry(self.SIDE_PANEL_RECT)
		# self.side_panel.setStyleSheet("QTextEdit{ background-image: url(media/notepad_images/notepad.png); }")

		# set up the main game panel
		self.main_panel = QWidget(self.window)
		self.main_panel.setGeometry(self.MAIN_PANEL_RECT)
		self.main_panel.setStyleSheet("QWidget{ background-image: url(media/office_background_images/officedefault.png);}")

	def show(self):
		self.page = QWebPage()
		self.view = QWebView()
		self.view.setPage(self.page)
		# self.window.setCentralWidget(self.view)

		mf = self.page.mainFrame()
		mf.load(QUrl("google.com"))
		self.window.show()
		sys.exit(self.app.exec_())

if __name__ == '__main__':
	game = WikiGame()
	game.show()
