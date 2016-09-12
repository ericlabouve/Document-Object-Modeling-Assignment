# Eric LaBouve
# CPE301 - Lab 4
# April 15th, 2016

from math import log

puncList = [".", ",", "?", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "[", "]", "{", "}", "-", "_", "=", "+", "\'", "\"", ":", ";" "/", "\\"]
wordexcPuncList = ["\'"]
numExcPuncList = ["$", "%", ".", ",", "-"]
kMaxTermFreq = 5

vocabWords = []
documents = []
authors = []

class TokenType(object):
	word = 1
	punctuation = 2
	number = 3
	other = 4

class Token(object):
	tokenValue = TokenType.other
	value = ""
	def __init__(self, tokenV, val):
		self.tokenValue = tokenV
		self.value = val 

class VocabWord(object):
	overallFreq = 1
	documentFreq = 1
	whichDocumentFreq = []
	word = ""
	def __init__(self, theWord, authorDir, author, authorNames):
		self.overallFreq = 1
		self.documentFreq = 1
		# Translation: [author1test, author1train, author2test ... author5train]
		self.whichDocumentFreq = [0,0,0,0,0,0,0,0,0,0] #2 slots per author (5 authors)
		self.word = theWord
		# Word is initially found in 1 document to had been created
		self.trackDocument(authorDir, author, authorNames)
	# Increments which document the word was found in 
	def trackDocument(self, authorDir, author, authorNames):
		authorIndex = 0
		# identify the author as an index in our authorNames. 
		# this corresponds to the index in our whichDocumentFreq list
		for index in range(len(authorNames)):
			if author == authorNames[index]:
				authorIndex = index * 2
				index = len(authorNames) # break from the loop
		#test are stored before train document in whichDocumentFreq
		if authorDir == "C50train":
			authorIndex += 1
		self.whichDocumentFreq[authorIndex] += 1

#Pre - Vocab list is completely filled out
class Author(object):
	name = ""	
#	filePath = ""
#	docs = []
	trainTermFreq = [] #indices correspond to the vocabulary word list
	testTermFreq = [] #indices correspond to the vocabulary word list
	trainMaxFreq = 1
	testMaxFreq = 1
	def __init__(self, namep): #, filePathp):
#		self.docs = []
		self.trainTermFreq = []
		self.testTermFreq = []
		self.name = namep
#		self.filePath = filePathp
		self.trainMaxFreq = 1
		self.testMaxFreq = 1	
	# Adds the document to the list of documents <-- NO
	# expands the term frequency lists
	# updates one of the term frequency lists
	# updates one of the MaxFreq's
	def addDoc(self, document):
#		self.docs.append(document)
		self.extendTermFreqList(self.trainTermFreq) # Avoid index out of bounds error
		self.extendTermFreqList(self.testTermFreq)
		self.updateTermFreq(document, document.docType)
	# Adds the document's termFreq[] to the author's corresponding termFreq[]
	# Updates the corresponding termFreq
	# Pre - termFreq lists lengths == vocabWords's length
	def updateTermFreq(self, document, docType):
		# test document
		if docType == 0:
			for i in range(len(document.termFreq)):
				self.testTermFreq[i] += document.termFreq[i]
				# update testMaxFreq
				if self.testTermFreq[i] > self.testMaxFreq:
					self.testMaxFreq = self.testTermFreq[i]
		# train document
		else:
			for k in range(len(document.termFreq)):
				self.trainTermFreq[k] += document.termFreq[k]
				# update testMaxFreq
				if self.trainTermFreq[k] > self.trainMaxFreq:
					self.trainMaxFreq = self.trainTermFreq[k]
	# extends termFreq list to length of the vocab list
	def extendTermFreqList(self, termFreq):
		# Difference is how many units we need to extend by
		difference = len(vocabWords) - len(termFreq)
		for i in range(difference):
			termFreq.append(0)

#Pre - Vocab list is up to date
class Document(object):
	name = ""
	filePath = ""
	author = ""
	docType = 0 	# 0 = test document; 1 = train document
	termFreq = [] #indices correspond to the vocabulary word list	
	def __init__(self, namep, filePathp, authorp, tokens):
		self.termFreq = []
		self.docType = 0
		self.name = namep
		self.filePath = filePathp
		self.author = authorp
		self.determineDocType()
		self.createTermFreqList(tokens)
	def determineDocType(self):
		# 0 = test document; 1 = train document
		# "test" is not found in the file path --> document is a train file
		if self.filePath.find("test") == -1:
			self.docType = 1
	def createTermFreqList(self, tokens):
		# Fill |termFreq| with all zeros with length=vocabWords.len()
		self.extendTermFreqList()
		# Go through tokens and update frequency of each token
		for i in range(len(tokens)):
			index = getVocabIndex(tokens[i].value)
			# Error check
			if index >= 0:
				self.termFreq[index] += 1
			else:
				print "Error in Document.class: createTermFreqList() Word not found in vocabWords: %s" % tokens[i].value
	# extends termFreq list to length of the vocab list
	def extendTermFreqList(self):
		# Difference is how many units we need to extend by
		difference = len(vocabWords) - len(self.termFreq)
		for i in range(difference):
			self.termFreq.append(0)

# Return index of a certain word in our vocab list
# Return -1 if word is not found
def getVocabIndex(compareWord):
	# Loop through all vocab words
	for i in range(len(vocabWords)):
		vword = vocabWords[i].word
		# If match
		if vword == compareWord:
			return i
	return -1 # Should never happen
	
# Turns a single file into a list of tokens
# parameter: filename (string) - name of/path to the file to be parsed
def tokenizer(filename):
	# Create empty list of parsed words
	parsedWords = []
	# Create empty list of tokens
	tokens = []
	# Open the file
	fp = open(filename)
	# Parse file by whitespace into parsed words list
	fileString = fp.read()
	for item in fileString.split(): #All white space
		parsedWords.append(item)
	# For each item in the parsed words list
	for item in parsedWords:
		# Convert to lower case
		item = item.lower()
		# Get list of tokens associated with the item
		tokenList = getToken(item)
		# For each item in the list of tokens associated with the item
		for tok in tokenList:
			# Add token to list of tokens
			tokens.append(tok)
	return tokens

# Takes as input a single chunk of text and 
# returns back a token that represents it
# (or tokens if more than one token is needed)
def getToken(chunk):
	tokenList = []

	## Handle Multiple Tockens within |chunk| ##
	# Check chunk[0] for punctuation token	
	for punc in puncList:
		# Matching punctuation that isn't a number punctuation
		if len(chunk) and punc == chunk[0] and chunk[0] != "$" and chunk[0] != "-":
			token = Token(TokenType.punctuation, punc)
			tokenList.append(token)
			# Take out punctuation from |chunk|
			chunk = chunk[1:]
			break
	# Check chunk[-1] for punctuation token
	for punc in puncList:
		if len(chunk) and punc == chunk[-1]:
			token = Token(TokenType.punctuation, punc)
			tokenList.append(token)
			# Take out punctuation from |chunk|
			chunk = chunk[:-1]
			break

	## Handle Remaining Characters in |chunk| ##
	# If |chunk| is just one word token
	if isWord(chunk):
		token = Token(TokenType.word, chunk)
		tokenList.append(token)
	# If |chunk| is just one number token
	elif isNumber(chunk):
		token = Token(TokenType.number, chunk)
		tokenList.append(token)
	# If |chunk| is just one punctuation token
	elif isPunctuation(chunk):
		token = Token(TokenType.punctuation, punc)
		tokenList.append(token)
	else:
		token = Token(TokenType.other, punc)
		tokenList.append(token)

	return tokenList

def isWord(chunkp):
	chunk = chunkp
	# Check if the word contains an apostrophe in the middle of the word
	if len(chunk) and chunk.find("\'") != -1:
		# remove any apostrophes
		chunk = chunk.replace("\'", "")
	return chunk.isalpha()

def isNumber(chunkp):
	chunk = chunkp
	# Check if the word contains a dollar sign or minu sign or percentage or comma
	if len(chunk) and chunk[0] == "$":
		# remove dollar sign
		chunk = chunk.replace(chunk[0], "")
	if len(chunk) and chunk[0] == "-":
		# remove dollar sign
		chunk = chunk.replace(chunk[0], "")
	if len(chunk) and chunk[-1] == "%":
		# remove any apostrophes
		chunk = chunk.replace(chunk[-1], "")
	if len(chunk) and chunk.find(",") != -1:
		# remove any apostrophes
		chunk = chunk.replace(",", "")
	return chunk.isdigit()

def isPunctuation(chunkp):
	chunk = chunkp
	# Must be one character long
	if len(chunk) > 1:
		return False
	# LOOP through all the different punctuation characters
	for pun in puncList:
		if pun in chunk:
			return True
	return False


def isNumberPunctuation(chunkp):
	chunk = chunkp
	# Must be one character long
	if len(chunk) > 1:
		return False
	# LOOP through all the different punctuation characters
	for pun in numExcPuncList:
		if pun in chunk:
			return True
	return False

# |tokenList| is the token list produced by tokenizer()
# Removes all non-word tokens
# Output: The list of word tokens from |tokenList|
def tokenCleanup(tokenList):
	outputList = []
	# Loop through all the tokens
	for token in tokenList:
		# IF token is a word
		if token.tokenValue == TokenType.word:
			# Add token to |outputList|
			outputList.append(token)
	return outputList

# |tokenList| is the list of tokens (usually, produced by tokenCleanup())
# |stopWordFilename| is name of/path to the file containing the list of stopwords
# checks, for each word token in the input token
# list if its content is on the liat of stopwords.
# If it is, the token is removed
# from the list. Otherwise, the token is placed in the output list
# Output: The list of non-stopword tokens from |tokenList|
def removeStopwords(tokenList, stopWordFilename):
	stopwords = []
	outputList = []
	fp = open(stopWordFilename)
	fileData = fp.read()
	# Fill out list of stop words in |stopwords|
	for word in fileData.split():
		stopwords.append(word)
	# Loop through all the tokens

	for token in tokenList:
		# IF token is not a stopword
		if isStopWord(token, stopwords) is False:
			# Add token to |outputList|
			outputList.append(token)
	return outputList

# |token| is token to be evaluated
# |stopwords| is list of stop words
# determines if the token is a stop word
def isStopWord(token, stopwords):
	for word in stopwords:
		if token.value == word:
			return True
	return False


def evaluateAuthor(rootDir, authorDir, author, authorNames):
	fileNames = []
	pathToFile = rootDir + "/" + authorDir + "/" + author + "/"
	pathToFileShort = authorDir + "/" + author + "/"
	# Open list of article names from |testDir| and compile the list of names
	fp = open(pathToFile + "fileNames.txt")
	# Read all article names into a list
	for txtFile in fp.read().split():
		fileNames.append(txtFile)
	fp.close()
	# For each article in the Dir
	for article in fileNames:
		### Generate token list ###
		tokens = tokenizer(pathToFile + article)
		tokens = tokenCleanup(tokens)
		tokens = removeStopwords(tokens, "stopwords.txt")
		appendVocabList(tokens, authorDir, author, authorNames)
		newDoc = Document(article, pathToFileShort, author, tokens)
		documents.append(newDoc)

#		break
#


# Adds unique vocab words to our vocabWords list
def appendVocabList(tokens, authorDir, author, authorNames):
	uniqueWords = {} #Map of unique token names
	# LOOP through all the tokens
	for token in tokens:		
		spot = getVocabIndex(token.value)
		# IF the word is in the vocab list
		if spot != -1:
			vocabWords[spot].overallFreq += 1
			# If this is the first occurance of this token in this document
			# ie token.value has not been added to our uniqueWords dictionary
			if not token.value in uniqueWords:
				vocabWords[spot].documentFreq += 1
				vocabWords[spot].trackDocument(authorDir, author, authorNames)
		else:
			vWordToAdd = VocabWord(token.value, authorDir, author, authorNames)
			vocabWords.append(vWordToAdd)
		uniqueWords[token.value] = 1 # Mark that token has been seen


def writeDocumentWeights(outFile):
	# open outFile for writing
	fp = open(outFile, "w")
	fp.write("path index:weight\n")
	# For each document we collected (500)
	for doc in documents:
		outString = doc.filePath + doc.name + " " # Path to file
		# For each word in each document
		for index in range(len(doc.termFreq)):
			# If the vocab word appears in the document
			if doc.termFreq[index] > 0:
				outString += str(index) + ":" # index of vocab word
				outString += str(calculate_tfidf_doc(doc, index)) # weight
				outString += " "
		outString += "\n"
		fp.write(outString)
	fp.close()

# Returns the tf-idf weight of a single word in a document
def calculate_tfidf_doc(doc, index):
	termFrequency = float(doc.termFreq[index])
	tfRatio = float(1)
	# Follow equation for tf:
	if termFrequency < kMaxTermFreq:
		tfRatio = (termFrequency / kMaxTermFreq)
	# Follow equation for idf:
	N = float(500) # number of total documents
	Nj = float(vocabWords[index].documentFreq) # number of documents that contain the term
	idfRatio = float(log(N/Nj, 2))
	return tfRatio * idfRatio

def fillAuthorsList(authorList):
	# Loop through all the authors
	for name in authorList:
		newAuthor = Author(name)
		authors.append(newAuthor)
		# Loop through all the documents
		for doc in documents:
			# If the document corresponds to the author
			if doc.author == name:
				newAuthor.addDoc(doc)


# Clears all the files in fileNames list and writes 
# the author vectors to these files
def writeAuthorWeights(fileNames):	
	# Clear all the files
	for theFile in fileNames:
		open(theFile, "w").close()
	# For each author
	for author in range(len(authors)):
		print "Starting author vector for %s" % authors[author].name
		writeVectorToFileFrom("test", fileNames[author], author)
		writeVectorToFileFrom("train", fileNames[author], author)


# @param whichDir - Either test or train. Author objects contain vector from these directories
# @param fileName - The file name to write to. 
# @param author - The index of the author we are evaluating
def writeVectorToFileFrom(whichDir, fileName, author):
	fp = open(fileName, "a")
	
	writeString = whichDir + "/" + authors[author].name + " "
	# Loop through all the vocabulary words
	for vocLoc in range(len(vocabWords)):
		wordWeight = calculate_tfidf_author(whichDir, author, vocLoc)
		# Only add elements that have significance
		if wordWeight > 0:
			writeString += str(vocLoc) + ":" + str(wordWeight) + " "
	writeString += "\n"
	fp.write(writeString)
	fp.close()

# @param whichDir - is either the test directory or the train directory
# @param author - index of author in authors list
# @param vocLoc - index of vocab word in vocabWords
# Calculates the tf-idf for author vector elements
def calculate_tfidf_author(whichDir, author, vocLoc):
	# W = tf * idf
	# tf = n / maxF
	# idf = Log2(N/Nj)
	whichDocFreqLoc = author * 2 #Location of test file for Nj
	if whichDir == "test":
		n = float(authors[author].testTermFreq[vocLoc])
		maxF = float(authors[author].testMaxFreq)
		
	else: # train
		n = float(authors[author].trainTermFreq[vocLoc])
		maxF = float(authors[author].trainMaxFreq)
		whichDocFreqLoc += 1 #train documents are located 1 index after test documents

	N = float(50)
	Nj = float(vocabWords[vocLoc].whichDocumentFreq[whichDocFreqLoc])
	tf = float(float(n) / float(maxF))
	idf = 0
	if Nj > 0:
		idf = float(log(float(N)/float(Nj), 2))
	return float(tf * idf)


def writeVocabWords(writeFile):
	fp = open(writeFile, "w")
	for inx in range(len(vocabWords)):
		writeString = vocabWords[inx].word + "\n"
		fp.write(writeString)
	fp.close()	

def writeAuthorData():
	fp = open("authorData.txt", "w")
	for iHateThisAssignment in authors:
		outString = "train/" + iHateThisAssignment.name + " "
		for count in iHateThisAssignment.trainTermFreq:
			outString += str(count) + " "
		outString += "\n"
		fp.write(outString)
		outString2 = "test/" + iHateThisAssignment.name + " "
		for count in iHateThisAssignment.testTermFreq:
			outString2 += str(count) + " "
		outString2 += "\n"
		fp.write(outString2)
	fp.close()

def main():
	rootDir = "C50"
	testDir = "C50test"
	trainDir = "C50train"
	fileNamestxt = "fileNames.txt" #names of all files separated by white space
	outFileDoc = "tf-idfWeightsDocuments.txt"
	outFileVoc = "vocabWords.txt"
	
	authorList = ["JoeOrtiz", "JonathanBirt", "MarkBendeich", "MureDickie", "RobinSidel"]
	authorVectorFileNames = ["JoeOrtizVectors.txt", "JonathanBirtVectors.txt", "MarkBendeichVectors.txt", "MureDickieVectors.txt", "RobinSidelVectors.txt"]

	#authorList = ["MureDickie"]
	#authorVectorFileNames = ["MureDickieVectors.txt"]

	# For each author
	for author in authorList:
		print "Starting author %s..." % author
		evaluateAuthor(rootDir, testDir, author, authorList)
		evaluateAuthor(rootDir, trainDir, author, authorList)

	# Extend term frequency of each document now that vocab list is filled
	for doc in documents:
		doc.extendTermFreqList()

#	print "Writing Document Weights..."
#	writeDocumentWeights(outFileDoc)


	fillAuthorsList(authorList)
#	writeAuthorWeights(authorVectorFileNames)

	print "Writing Author Data to authorData.txt"
	writeAuthorData()

#	print "Writing Vocab Words"
	writeVocabWords(outFileVoc)

	print "Done"

	



### Bellow are methods to print a few data types ###

def printTokens(tokens):
	for token in tokens:
		if token.tokenValue == 1:
			print "Word:%s" % token.value
		elif token.tokenValue == 2:
			print "Punctuation:%s" % token.value
		elif token.tokenValue == 3:
			print "Number:%s" % token.value
		else:
			print "Other:%s" % token.value

def printVocabList():
	totalWords = 0
	totalFreq = 0
	for vWord in vocabWords:
		print "%s %d %d" % (vWord.word, vWord.overallFreq, vWord.documentFreq)
		print "(%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)" % (vWord.whichDocumentFreq[0],vWord.whichDocumentFreq[1],vWord.whichDocumentFreq[2],vWord.whichDocumentFreq[3],vWord.whichDocumentFreq[4],vWord.whichDocumentFreq[5],vWord.whichDocumentFreq[6],vWord.whichDocumentFreq[7],vWord.whichDocumentFreq[8],vWord.whichDocumentFreq[9])
		sum = 0
		for item in range(len(vWord.whichDocumentFreq)):
			sum += vWord.whichDocumentFreq[item]
		print "%s\n" % (sum == vWord.documentFreq)
		totalWords += 1
		totalFreq += vWord.overallFreq
	print "TotalVocWords=%d, totalFreq=%d" % (totalWords, totalFreq)

def printDocuments():
	for doc in documents:
		print "\n\n"
		doc.extendTermFreqList()
		print "name=%s" % doc.name
		print "filePath=%s" % doc.filePath
		print "docType=%s" % ("test" if doc.docType == 0 else "train")
		for i in range(len(doc.termFreq)):
			print "%s=%d" % (vocabWords[i].word, doc.termFreq[i])





### Bellow are tests to verify the quality of some of the helper functions above ###

def test():
	# Test of isWord
	print "* Test isWord()"
	print "Exp: True, Act: %s" % isWord("eric") #true
	print "Exp: True, Act: %s" % isWord("erics") #true
	print "Exp: True, Act: %s" % isWord("eric's") #true
	print "Exp: True, Act: %s" % isWord("'eric") #true
	print "Exp: True, Act: %s" % isWord("'eric'") #true
	print "Exp: True, Act: %s" % isWord("eric'") #true
	print "Exp: False, Act: %s" % isWord("er.ic'") #false
	print "Exp: False, Act: %s" % isWord("'") #false
	print "Exp: False, Act: %s" % isWord("%") #false

	# Test of isNumber
	print "* Test isNumber()"
	print "Exp: True, Act: %s" % isNumber("123456789") #true
	print "Exp: True, Act: %s" % isNumber("$123456789") #true
	print "Exp: True, Act: %s" % isNumber("$123,456,789") #true
	print "Exp: True, Act: %s" % isNumber("19%") #true
	print "Exp: True, Act: %s" % isNumber("-8796") #true
	print "Exp: False, Act: %s" % isNumber("19a") #false
	print "Exp: False, Act: %s" % isNumber("$") #false
	print "Exp: False, Act: %s" % isNumber(",") #false
	print "Exp: False, Act: %s" % isNumber("%") #false
	print "Exp: False, Act: %s" % isNumber("'") #false
	print "Exp: False, Act: %s" % isNumber("-") #false

	# Test of isPunctuation
	print "* Test isPunctuation()"
	print "Exp: True, Act: %s" % isPunctuation("$") #true
	print "Exp: False, Act: %s" % isPunctuation("~") #false

	# Test of isStopWord
	print "* Test isStopWord()"
	stopwords = []
	fp = open("stopwords.txt")
	fileData = fp.read()
	# Fill out list of stop words in |stopwords|
	for word in fileData.split():
		stopwords.append(word)
	token1 = Token(TokenType.word, "a")
	token2 = Token(TokenType.word, "i")
	token3 = Token(TokenType.word, "eric")
	token4 = Token(TokenType.word, "basketball")
	print "Exp: True, Act: %s" % isStopWord(token1, stopwords) #true
	print "Exp: True, Act: %s" % isStopWord(token2, stopwords) #true
	print "Exp: False, Act: %s" % isStopWord(token3, stopwords) #false
	print "Exp: False, Act: %s" % isStopWord(token4, stopwords) #false

#test()
main()
