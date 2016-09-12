# Generates and stores the data needed for the word clouds

from operator import attrgetter

class Word():
	word = ""
	freq = 0
	def __init__(self, wordp, freqp):
		self.word = wordp
		self.freq = freqp
	def __str__(self):
		return str(self.freq) + " " + self.word
	def __lt__(self, other):
		return self.freq < other.freq

def main():
	inFile = "authorData.txt"
	vocFile = "vocabWords.txt"
	outDirFiles = ["top40JoeOrtizTrain.txt", "top40JoeOrtizTest.txt",
				"top40JonathanBirtTrain.txt", "top40JonathanBirtTest.txt",
				"top40MarkBendeichTrain.txt", "top40MarkBendeichTest.txt",
				"top40MureDickieTrain.txt", "top40MureDickieTest.txt",
				"top40RobinSidelTrain.txt", "top40RobinSidelTest.txt"]
					
	outAuthorFiles = ["top40JoeOrtiz.txt",
					  "top40JonathanBirt.txt",
					  "top40MarkBendeich.txt",
					  "top40MureDickie.txt",
					  "top40RobinSidel.txt"]

	vocfp = open(vocFile, "r")
	vocList = vocfp.read().split()
	vocfp.close()

	infp = open(inFile, "r")
	inData = infp.read().split("\n")
	infp.close()



	# JoeOrtiz
	JoeOrtizTrain = convert(inData[0], vocList)
	JoeOrtizTrain40 = generageList(JoeOrtizTrain)
	write(JoeOrtizTrain40, outDirFiles[0])
	JoeOrtizTest = convert(inData[1], vocList)
	JoeOrtizTest40 = generageList(JoeOrtizTest)
	write(JoeOrtizTest40, outDirFiles[1])
	JoeOrtiz40 = trim(JoeOrtizTrain40, JoeOrtizTest40)
	JoeOrtiz40 = generageList(JoeOrtiz40)
	write(JoeOrtiz40, outAuthorFiles[0])

	# JonathanBirt
	JonathanBirtTrain = convert(inData[2], vocList)
	JonathanBirtTrain40 = generageList(JonathanBirtTrain)
	write(JonathanBirtTrain40, outDirFiles[2])
	JonathanBirtTest = convert(inData[3], vocList)
	JonathanBirtTest40 = generageList(JonathanBirtTest)
	write(JonathanBirtTest40, outDirFiles[3])
	JonathanBirt40 = trim(JonathanBirtTrain40, JonathanBirtTest40)
	JonathanBirt40 = generageList(JonathanBirt40)
	write(JonathanBirt40, outAuthorFiles[1])

	# MarkBendeich
	MarkBendeichTrain = convert(inData[4], vocList)
	MarkBendeichTrain40 = generageList(MarkBendeichTrain)
	write(MarkBendeichTrain40, outDirFiles[4])
	MarkBendeichTest = convert(inData[5], vocList)
	MarkBendeichTest40 = generageList(MarkBendeichTest)
	write(MarkBendeichTest40, outDirFiles[5])
	MarkBendeich40 = trim(MarkBendeichTrain40, MarkBendeichTest40)
	MarkBendeich40 = generageList(MarkBendeich40)
	write(MarkBendeich40, outAuthorFiles[2])

	# MureDickie
	MureDickieTrain = convert(inData[6], vocList)
	MureDickieTrain40 = generageList(MureDickieTrain)
	write(MureDickieTrain40, outDirFiles[6])
	MureDickieTest = convert(inData[7], vocList)
	MureDickieTest40 = generageList(MureDickieTest)
	write(MureDickieTest40, outDirFiles[7])
	MureDickie40 = trim(MureDickieTrain40, MureDickieTest40)
	MureDickie40 = generageList(MureDickie40)
	write(MureDickie40, outAuthorFiles[3])

	# RobinSidel
	RobinSidelTrain = convert(inData[8], vocList)
	RobinSidelTrain40 = generageList(RobinSidelTrain)
	write(RobinSidelTrain40, outDirFiles[8])
	RobinSidelTest = convert(inData[9], vocList)
	RobinSidelTest40 = generageList(RobinSidelTest)
	write(RobinSidelTest40, outDirFiles[9])
	RobinSidel40 = trim(RobinSidelTrain40, RobinSidelTest40)
	RobinSidel40 = generageList(RobinSidel40)
	write(RobinSidel40, outAuthorFiles[4])

#Combines words that are found more than once
def trim(list1, list2):
	for word in list1:
		for otherWord in list2:
			if word.word == otherWord.word:
				word.freq += otherWord.freq
	return list1


def write(JoeOrtizTrain40, outDirFile):
	fp = open("wordCloud/" + outDirFile, "w")
	count = 1
	for item in JoeOrtizTrain40:
		outString = item.__str__()
		count += 1
		if count < 40:
			outString += "\n"		
		fp.write(outString)
	fp.close()


def generageList(convertedList):
	list40 = []
	i = 0
	for item in sorted(convertedList, key=attrgetter("freq"), reverse=True):
		if i >= 40:
			break;
		list40.append(item)
		i += 1
	return list40


#	JoeOrtizTest = inData[1]
#	JonathanBirtTrain = inData[2]
#	JonathanBirtTest = inData[3]
#	MarkBendeichTrain = inData[4]
#	MarkBendeichTest = inData[5]
#	MureDickieTrain = inData[6]
#	MureDickieTest = inData[7]
#	RobinSidelTrain = inData[8]
#	RobinSidelTest = inData[9]

def convert(inString, vocList):
	elementNum = -1
	elements = inString.split()
	wordList = []
	for elemSpot in range(len(elements)):
		if elementNum >= 0 and int(elements[elemSpot]) > 0:
			word = Word(str(vocList[elemSpot - 1]), int(elements[elemSpot]))
			wordList.append(word)
		elementNum += 1
	return wordList

def printList(list):
	count = 1
	for item in list:
		print str(count) + ") " + item.__str__()
		count += 1



main()