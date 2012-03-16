from __builtin__ import hex as pyhex	# because apparently PyQt4 overrides hex()
import os   # for searching the office_background_images directory
import sys
import signal
from WebRenderer import WebRenderer
from WikiData import WikiData

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

import Image	# PIL module for image manipulation
office_chromatic_map = Image.open('media/office_background_images/officechromaticmap.png')  # The Image file that contains the chromatic map
main_panel = None   # Dirty hack to allow us access to the main_panel in the below functions. TODO: Remove dirty hack.
office_images = os.listdir('media/office_background_images')	# A list of all of the images in the office_background_images directory
cursor = None   # Mouse cursor. Needs to be global because of the unfortunate way that the main_panel is implemented. TODO: Remove dirty hack.

def mainPanelMouseMoveEvent(event):
#
# Creating a subclass of QWidget (which is what I wanted to do in order to override the default mouseMoveEvent method of the main_panel QWidget) apparently breaks the setStyleSheet method (which I need in order to set a background image, since I couldn't figure out any other way to do that). 
# Therefore, since I cannot subclass QWidget, my only other option was to create a function with the same functionality, and then assign it to the method.
# TODO: Remove dirty hack.
# jmoldow, 2012/03/15
#
	global main_panel, office_images, cursor
	color = getColor(event)
	if ('office%s.png' % color) in office_images:   # if there is a background image overlay for that chromatic map color
		setBackgroundImage(main_panel,'media/office_background_images/office%s.png' % color)	# overlay a new background image
		cursor.setShape(Qt.PointingHandCursor)  # Change to the pointing hand cursor
	else:
		clearBackgroundImage(main_panel)	# clear the overlayed image, make the main_panel transparent
		cursor.setShape(Qt.ArrowCursor) # Return to the default cursor
	main_panel.setCursor(cursor)	# Reassign the cursor to the main_panel

def getColor(event):
	'''
Function that returns the Hex string (without the leading 0x) of the color of the chromatic map at the position of the mouse event.
	'''
	global office_chromatic_map
	pos = event.pos()   # the position of the mouse, as a QPoint
	pos = (pos.x(), pos.y())	# the position of the mouse, as a 2-tutple of integers
	return ''.join(map(lambda x: ('0'+pyhex(int(x))[2:].upper())[-2:], office_chromatic_map.getpixel(pos)[0:3]))   # The Hex string (without the leading 0x) of the color of the chromatic map at that mouse position

colors = {} # A dictionary that maps labels for the different types of clickables to a tuple of their colors in the chromatic map
colors['exit'] = ('00FF00',)
colors['menu'] = ('FF0000',)
colors['files'] = ('000088','008800','880000')
colors['photos'] = ('FFFF88','FF0088','88FF00')
colors['gun'] = ('FF8800',)
colors['open_folder'] = ('8800FF',)
colors['name_plate'] = ('FF88FF',)
colors['globe'] = ('0088FF',)
colors['fox'] = ('00FF88',)

def mainPanelMousePressEvent(event):
# See my comments for mainPanelMouseMoveEvent
	global main_panel, cursor
	color = getColor(event)
	if color in colors['exit']: # exit lamp
		sys.exit()
	elif color in colors['menu']: # main menu
		pass
	elif color in colors['files']:   # files
		pass
	elif color in colors['photos']:
		pass
	elif color in colors['gun']:
		pass
	elif color in colors['open_folder']:
		pass
	elif color in colors['name_plate']:
		pass
	elif color in colors['globe']:
		pass
	elif color in colors['fox']:
		pass
	else:
		pass

def setBackgroundImage(widget, url):
	'''
Set the background image for widget, using the image located at url (which is a string giving the relative location of the image file).
	'''
	widget.setStyleSheet("QWidget{ background-image: url(%s);}" % url)

def clearBackgroundImage(widget):
	'''
Clear the background image for widget, set the background color as transparent.
	'''
	widget.setStyleSheet("QWidget{ background-image: none; background-color: transparent; }")

class WikiGame:
	def __init__(self):
		global main_panel, cursor   # Dirty hack to allow us to refer to the main_panel, cursor in the above functions. TODO: Remove dirty hack.
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
		cursor = QCursor(Qt.ArrowCursor)
		self.window.setCursor(cursor)

		# set up the notepad side panel
		self.side_panel = QTextEdit(QString(u'Your Detective Notepad<br /><br /><br />'), self.window)
		self.side_panel.setGeometry(self.SIDE_PANEL_RECT)
		# self.side_panel.setStyleSheet("QTextEdit{ background-image: url(media/notepad_images/notepad.png); }")

		# Set up the background of the main panel. This widget is useless, except for displaying the background and being the parent widget of the actual main_panel
		self.main_panel_background = QWidget(self.window)
		self.main_panel_background.setGeometry(self.MAIN_PANEL_RECT)
		setBackgroundImage(self.main_panel_background, 'media/office_background_images/officedefault.png')

		# set up the main game panel
		main_panel = self.main_panel = QWidget(self.main_panel_background) # Dirty hack to allow us to refer to the main_panel in the above functions. TODO: Remove dirty hack.
		self.main_panel.setGeometry(self.MAIN_PANEL_RECT)
		clearBackgroundImage(self.main_panel)
		self.main_panel.setMouseTracking(True)  # Makes it so that MouseMove events are triggered whenever the mouse moves, regardless of whether the button is being held.
		self.main_panel.mouseMoveEvent = mainPanelMouseMoveEvent	# Set the above-defined function as a static object method. TODO: Remove dirty hack.
		self.main_panel.setCursor(cursor)
		self.main_panel.mousePressEvent = mainPanelMousePressEvent

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
