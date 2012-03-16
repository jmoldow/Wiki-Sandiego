from __builtin__ import hex as pyhex	# because apparently PyQt4 overrides hex()
import os   # for searching the office_background_images directory
import sys
import signal
from WebRenderer import WebRenderer
from WikiData import WikiData
from Game import Game

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

import Image	# PIL module for image manipulation
office_chromatic_map = Image.open('media/office_background_images/officechromaticmap.png')  # The Image file that contains the chromatic map
main_panel = None   # Dirty hack to allow us access to the main_panel in the below functions. TODO: Remove dirty hack.
main_menu = None	# Global variable for accessing the main_menu in the below functions.
instructions = None # Global variable for accessing the instructions in the below functions.
office_images = os.listdir('media/office_background_images')	# A list of all of the images in the office_background_images directory
cursor = None   # Mouse cursor. Needs to be global because of the unfortunate way that the main_panel is implemented. TODO: Remove dirty hack.
game = Game()   # Global variable that stores the game
opened_windows = [] # List of windows that are (or have in the past been) opened. This is so that the displayed pop-ups aren't immediately destroyed by Python when the local variable goes out of scope

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

def getPos(event):
	'''
Function that returns a tuple of the position of the mouse event.
	'''
	pos = event.pos() # the position of the mouse, as a QPoint
	return (pos.x(), pos.y()) # the position of the mouse, as a 2-tutple of integers

def getColor(event):
	'''
Function that returns the Hex string (without the leading 0x) of the color of the chromatic map at the position of the mouse event.
	'''
	global office_chromatic_map
	pos = getPos(event)   # the position of the mouse, as a 2-tutple of integers
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
	global main_panel, main_menu, cursor, game, opened_windows
	color = getColor(event)
	widget = None   # The widget returned by the clickable
	if color in colors['exit']: # exit lamp
		sys.exit()
	elif color in colors['menu']: # main menu
		game.restart()  # Returning to the menu should restart the game
		main_menu.raise_() # hide the menu behind everything else

	elif color in colors['files']:   # files
		widget = game.showClue(colors['files'].index(color))	# Clicking on a folder returns a clue widget
	elif color in colors['photos']:
		widget = game.showClipping(colors['photos'].index(color))   # Clicking on a photo returns a clipping widget
	elif color in colors['gun']:
		pass
	elif color in colors['open_folder']:
		widget = game.showClue(4)   # The open folder was supposed to be special, but now it's not, so return a different clue widget
	elif color in colors['name_plate']:
		pass
	elif color in colors['globe']:
		widget = game.showWikipedia()   # Clicking on the globe opens Wikipedia
	elif color in colors['fox']:
		pass
	else:
		pass
	if widget:  # If the clickable has a widget associated with it
		opened_windows.append(widget)   # Store the widget so it doesn't go out of scope
		opened_windows[-1].show()   # show the widget

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

menu_buttons = {}   # Dictionary that maps labels for the menu buttons to rectangles describing their positions
menu_buttons['play'] = QRect(QPoint(70,570),QPoint(180,645))
menu_buttons['instructions'] = QRect(QPoint(220,570),QPoint(485,645))
menu_buttons['exit'] = QRect(QPoint(525,570),QPoint(640,645))

def mainMenuMouseMoveEvent(event):
	global menu_buttons, main_menu
	pos = event.pos()
	in_button = False
	for label,rect in menu_buttons.iteritems():
		if rect.contains(pos):
			cursor.setShape(Qt.PointingHandCursor)  # Change to the pointing hand cursor
			in_button = True
	if not in_button:
		cursor.setShape(Qt.ArrowCursor) # Return to the default cursor
	main_menu.setCursor(cursor)

def mainMenuMousePressEvent(event):
	global menu_buttons, main_menu, instructions
	pos = event.pos()
	if menu_buttons['play'].contains(pos):
		main_menu.lower()
		instructions.lower()
	elif menu_buttons['instructions'].contains(pos):
		main_menu.lower()
		instructions.raise_()
	elif menu_buttons['exit'].contains(pos):
		sys.exit()

return_to_menu = QRect(QPoint(570,560),QPoint(685,650))

def instructionsMouseMoveEvent(event):
	global instructions, return_to_menu
	pos = event.pos()
	if return_to_menu.contains(pos):
		cursor.setShape(Qt.PointingHandCursor)  # Change to the pointing hand cursor
	else:
		cursor.setShape(Qt.ArrowCursor) # Return to the default cursor
	instructions.setCursor(cursor)

def instructionsMousePressEvent(event):
	global instructions, main_menu, return_to_menu
	pos = event.pos()
	if return_to_menu.contains(pos):
		instructions.lower()
		main_menu.raise_()

class WikiGame:
	def __init__(self):
		global main_panel, main_menu, instructions, cursor   # Dirty hack to allow us to refer to the main_panel, cursor in the above functions. TODO: Remove dirty hack.
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

		# set up the main menu
		main_menu = self.main_menu = QWidget(self.window)
		self.main_menu.setGeometry(self.MAIN_PANEL_RECT)
		setBackgroundImage(self.main_menu, 'media/menu/menu.png')
		self.main_menu.setMouseTracking(True)
		self.main_menu.setCursor(cursor)
		self.main_menu.raise_()
		self.main_menu.mouseMoveEvent = mainMenuMouseMoveEvent
		self.main_menu.mousePressEvent = mainMenuMousePressEvent

		# set up the instructions page
		instructions = self.instructions = QWidget(self.window)
		self.instructions.setGeometry(self.MAIN_PANEL_RECT)
		setBackgroundImage(self.instructions, 'media/menu/instructions.png')
		self.instructions.setMouseTracking(True)
		self.instructions.setCursor(cursor)
		self.instructions.lower()
		self.instructions.mouseMoveEvent = instructionsMouseMoveEvent
		self.instructions.mousePressEvent = instructionsMousePressEvent

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
	wikigame = WikiGame()
	wikigame.show()
