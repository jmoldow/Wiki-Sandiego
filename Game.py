from WikiData import *
from QtGui import *
class Game:
	def __init__(self):
		self.restart()

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
		wv.setUrl(QUrl("http://en.wikipedia.org/wiki/" + clip[1]))
		return wv
		

	def checkAnswer(self, answer):
		loc =  [c for c in self.location.lower() if 'a'<=c<='z']
		loc2 = [c for c in        answer.lower() if 'a'<=c<='z']
		return loc == loc2

	def numClues(self):
		return len(self.clueTitles)

	def numClippings(self):
		return len(self.clippings)

	def restart(self):
		self.wd = WikiData()
		[self.location, self.clueTitles, self.clippings] = self.wd.initializeGame()

if __name__=="__main__":
	g = Game()

