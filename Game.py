
class Game:
	def __init__(self):
		self.restart()

	def showClue(self, num):
		clue = self.clueTitles[num]
		pass

	def showClipping(self, num):
		clip = self.clippings.items()[num]
		pass

	def checkAnswer(self, answer):
		loc =  [c for c in self.location.lower() if 'a'<=c<='z']
		loc2 = [c for c in        answer.lower() if 'a'<=c<='z']
		return loc == loc2

	def numClues(self):
		return len(self.clueTitles)

	def numClippings(self):
		return len(self.clippings)

	def restart():
		self.wd = WikiData()
		[self.location, self.clueTitles, self.clippings] = self.wd.initializeGame()
