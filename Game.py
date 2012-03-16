import sys

from WikiData import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *


class Game:
    def __init__(self):
        self.wd = WikiData()
        self.restart()

    def showWikipedia(self):
        wv = QWebView()

        wv.setWindowTitle("Wikipedia")
        wv.setUrl(QUrl("http://en.wikipedia.org/wiki/"))

    def showClue(self, num):
        clue = self.clueTitles[num]
        wv = QWebView()
        wv.setWindowTitle(clue)
        wv.setUrl(QUrl("http://en.wikipedia.org/wiki/" + clue))
        return wv

    def showClipping(self, num, width=400, height=400):
        clip = self.clippings.items()[num]
        CLIPPING_RECT = QRect(QPoint(0,0), QPoint(width, height))
        IMAGE_RECT = QRect(QPoint(0,0), QSize(width,3*height/4))
        CAPT_RECT = QRect(QPoint(0, 3*height/4), QPoint(width, height))
        mw = QWidget()
        mw.setGeometry(CLIPPING_RECT)
        mw.setWindowTitle(clip[0])
        capt = QTextEdit(mw)
        capt.setHtml(clip[0])
        capt.setReadOnly(True)
        capt.setGeometry(CAPT_RECT)
        wv = QWebView(mw)
        wv.setWindowTitle(clip[0])
        wv.setGeometry(IMAGE_RECT)
        image = ""
        if len(clip[1]) > 0:
            image = clip[1][0]
        wv.setUrl(QUrl("http://en.wikipedia.org/wiki/" + clip[0]))
        return mw


    def checkAnswer(self, answer):
        loc =  [c for c in self.location.lower() if 'a'<=c<='z']
        loc2 = [c for c in        answer.lower() if 'a'<=c<='z']
        self.tries -= 1
        return loc == loc2

    def numClues(self):
        return len(self.clueTitles)

    def numClippings(self):


        return len(self.clippings)

    def guessesLeft(self):
        return self.tries

    def restart(self):
        [self.location, self.clueTitles, self.clippings] = self.wd.initializeGame()
        self.tries = 3

def validNum(s):
    s = s.strip()
    try:
        return int(s)
    except ValueError:
        return -1

def printHelp(g):
    print "In order to catch Cujo, you'll have to carefully examine the clues and clipping he's sent you.\n" + \
        "\tTo look at a Clue, type C# (Where # is between 1 and " + str(g.numClues()) + ")\n" + \
        "\tTo look at a Clipping, type L# (Where # is between 1 and " + str(g.numClippings()) + ")\n" + \
        "\tIf you know where Cujo is, type A XYZ (Where XYZ is the location that Cujo is currently at)\n" + \
        "\tTo give up, type Q\n" + \
        "\tTo see this help again, type ?\n"

def runGame():
    g = Game()
    print "----------------------------------------------------------------------------------"
    print "You are David A. Honig, an investigator in the International Art Crime Unit of"
    print "the UN. In an unprecedented event, your unit has received 11 (22/2) messages from"
    print "Cujo Sanfran, a famous Art Thief, clueing the locations where he will be pulling"
    print "off a major heist in the coming days. It is up to you to stop him, before he steals"
    print "the masterpieces from around the world.\n\n"

    total = 11
    r = total
    win = 0
    while r > 0:
        print "\n\nMasterpiece " + str(total - r + 1) + ": \n"
        if r == total:
            print "Cujo has sent you messages indicating where he is going to strike. It's up to you"
        else:
            print "Cujo has sent you another message indicating where he's going to strike next. It's up to you"            
        print "to figure out where his next target is going to be."
        print "Good Luck!\n\n"
        gameOver = False

        printHelp(g)
        while not gameOver:
            
            inp = raw_input(">") + " "
            if inp[0].upper() == 'Q':
                r = 0
                break
            if inp[0].upper() == 'C' and validNum(inp[1:]) > 0 and validNum(inp[1:]) <= g.numClues():
                num = validNum(inp[1:]) - 1
                w = g.showClue(num)
                w.show()
                print g.clueTitles[num]
            elif inp[0].upper() == 'L' and validNum(inp[1:]) > 0 and validNum(inp[1:]) <= g.numClippings():
                num = validNum(inp[1:]) - 1
                w = g.showClipping(num)
                w.show()
                print g.clippings.items()[num]
            elif inp[0].upper() == 'A':
                answer = inp[1:]
                if g.checkAnswer(answer):
                    print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
                    print "Congragulations, you've discovered where Cujo is going to strike next. There is no way that Cujo can get to the"
                    print "artwork, now that you've sent agents to that area. However, you still haven't caught Cujo yet."
                    print g.location + "'s masterpieces are now safe thanks to you!"
                    gameOver = True
                    win += 1
                    g.restart()
                else:
                    if g.guessesLeft() > 0:
                        print "Cujo doesn't seem to have made any plans to steal the art from there, there isn't much time left, hopefully"
                        print "you can figure out where he's going to strike before he does.  (" + str(g.guessesLeft()) + " Tries Left)"
                    else:
                        print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
                        print "Oh no, Cujo has stolen a masterpiece from " + g.location + "! Hopefully, you can stop him next time."
                        g.restart()
                        gameOver = True
            elif inp[0] == '?':
                printHelp(g)
            else:
                print "What was that again: (To see help, type '?')"

        r -= 1

    if win >= total:
        print "You've caught a break, after stopping Cujo all 11 times, you finally caught up to him" + \
                "in the last country. Now, he's behind bars, and he'll never have a chance to steal again."
        print "YOU WIN!!!"
    elif win > total / 2:
        print "You've managed to stop Cujo from stealing most of the artwork he set off to steal. Great Job!"
        print "After this, you wouldn't be surprised if you got a promotion!"
        print "You recovered " +str(win) + " out of " + str(total) + " masterpieces. Congragulations!"
    else:
        print "It seems that Cujo got the better of you and the rest of IACU, better luck next time."
        print "You only recovered " + str(win) + " out of " + str(total) + " masterpieces."


if __name__=="__main__":
    a = QApplication([''])
    print "Where in the Wiki\n"
    print "A Game by Dexter Cogswell, Jordan Moldow, Steven Valdez, and Zandra Vinegar"
    print "Data and Images from Wikipedia (http://en.wikipedia.org/wiki/Wikipedia:Copyrights)"
    while True:
        runGame()

        print "To START GAME, type 'P'. Otherwise, hit ENTER to quit."
        i = raw_input(">")
        if len(i) ==  0 or i[0].upper() != 'P':
            sys.exit(0)
