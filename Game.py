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

    def showClipping(self, num):
        clip = self.clippings.items()[num]
        wv = QWebView()
        wv.setWindowTitle(clip[0])
        image = ""
        if len(clip[1]) > 0:
            image = clip[1][0]
        wv.setUrl(QUrl("http://en.wikipedia.org/wiki/" + clip[0]))
        return wv


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

if __name__=="__main__":
    a = QApplication([''])
    g = Game()
    print "Hello, and welcome to the Wiki Enrichment Center."
    while True:
        print "In order to catch the crook, you'll have to carefully examine the clues.\n" + \
              "\tTo Quit, type Q\n" + \
              "\tTo look at a clue, type C# (Where # is between 1 and " + str(g.numClues()) + ")\n" + \
              "\tTo look at a clipping, type L# (Where # is between 1 and " + str(g.numClippings()) + ")\n" + \
              "\tIf you know where the crook is, type A * (Where * is the location of the crook)"

        inp = raw_input(">")
        if inp[0].upper() == 'Q':
            break
        if inp[0].upper() == 'C':
            num = int(inp[1:]) - 1
            w = g.showClue(num)
            w.show()
            print g.clueTitles[num]
        elif inp[0].upper() == 'L':
            num = int(inp[1:]) - 1
            w = g.showClipping(num)
            w.show()
            print g.clippings.items()[num]
        elif inp[0].upper() == 'A':
            answer = inp[1:]
            if g.checkAnswer(answer):
                print "Congragulations, the crook was in " + g.location + "! And, thanks to you, we've caught them."
                print "Unfortunately, there seems to be another crook on the loose."
                g.restart()
            else:
                if g.guessesLeft() > 0:
                    print "No one was there when we went to check, stop wasting our time. (" + str(g.guessesLeft()) + " Tries Left)"
                else:
                    print "The art has been STOLEN!!! You've lost. However, there's another crook you may be able to catch."
                    g.restart()
        else:
            print "What did you say?" + g.location


