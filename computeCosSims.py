#Single Author Comparisons - For each directory. Between each pair of articles.
#	Retain: Largest, Smallest, Average, and Standard Deviation of all Simularities
#
#Single Author Comparisons between subsets - For each pair of directories test:train set 
#											 representing the work of the same author.
#	
#
#Comparison of Different Authors:

from collections import OrderedDict
from math import sqrt
import numpy as np # Contains standard deviation func std

# "Given the path to a .txt file, you are handed a vector representing that file"
# key = path to file: /Directory/author/file 
#		Example: C50test/JoeOrtiz/379335newsML.txt
# value = Dictionary representing the vector
# 
# 					vector	
# filePath:		(0:1.342, 1:0.245, 2:0.998, ...)
# filePath:		(1:1.342, 4:0.245, 7:0.998, ...)
#  ... 				 ...
# filePath:		(0:2.352, 4:0.255, 6:0.088, ...)
#
class VecorMap():
	#{KEY=path : VALUE={KEY=vocInx : VALUE=weight}}
	vectors = OrderedDict()

	# Fills out |vectors| by scanning the passed in |vectorLocation| file
	# @param vectorLocation - File that contains all the vectors
	def __init__(self, vectorLocation):
		# Read in each vector:
		f = open(vectorLocation, "r")
		lineNum = 1 #First line doesnt contain vector data			
		# Loop through each line, which contains a single text file vector
		for line in f:
			KEYfilePath = ""
			VALUEvectorElements = OrderedDict() #Dictionary for |vectors|' VALUE 
			# Extract vector data
			if lineNum > 1:
				elementNumber = 1 #First element contains file path
				lineData = line.split(" ")
				# Loop through all the idx:weight's in |lineData|
				for item in lineData:    					
					if elementNumber == 1: # Extract file path
						KEYfilePath = item
						elementNumber += 1
					else: # Extract Key=VocIndx Value=Weight
						idx_weight = item.split(":")
						# Vocab Word Index : Weight
						if not idx_weight[0] == '\n': # Last line in file may be newline
							VALUEvectorElements[int(idx_weight[0])] = float(idx_weight[1])
				self.vectors[KEYfilePath] = VALUEvectorElements
			# Do nothing (Skip first line)
			else:
				lineNum += 1
			
		f.close()
    # String representation of our VectorMap
	def __str__(self):
		string = ""
		for pathKey in self.vectors.keys():
			string += pathKey + " "
			for idxKey in self.vectors[pathKey].keys():
				string += str(idxKey) + ":" + str(self.getWeightAt(pathKey, idxKey)) + " "
			string += "\n"
		return string
	# Returns an ordered list of file path keys
	def getPathKeys(self):
		return self.vectors.keys()
	# Returns an ordered list of vocab indexes given a Path Key
	def getIndexKeys(self, pathKey):
		return self.vectors[pathKey].keys()
	# Returns a vector given a path
	def getVectorAt(self, path):
		return self.vectors[path]
	# Returns the weight given a specified path key and index key
	def getWeightAt(self, pathKey, indexKey):
		return (self.vectors[pathKey])[indexKey]

class DocData():
	mx = 0.0
	mn = 1.0
	avg = 0.0
	stdev = 0.0
	def __init__(self, x1, x2, x3, x4):
		self.mx = x1
		self.mn = x2
		self.avg = x3
		self.stdev = x4
	def __str__(self):
		return "max=%f min=%f avg=%f stdev=%f\n" % (self.mx,self.mn,self.avg,self.stdev)


def main():
	authorVectorsFile = "tf-idfWeightsAuthors.txt"
	documentVectorFile = "tf-idfWeightsDocuments.txt"
	documentAnalysisOutFile = "documentAnalysis.txt"
	docOutFile = "documentCosSims.txt"
	AuthorOutFile = "authorCosSims.txt"

	authorList = ["JoeOrtiz", "JonathanBirt", "MarkBendeich", "MureDickie", "RobinSidel"]
	
	fileWeightsByDirList = ["tf-idfWeightsJoeOrtizTest.txt", "tf-idfWeightsJoeOrtizTrain.txt", 
				"tf-idfWeightsJonathanBirtTest.txt", "tf-idfWeightsJonathanBirtTrain.txt", 
				"tf-idfWeightsMarkBendeichTest.txt", "tf-idfWeightsMarkBendeichTrain.txt",
				"tf-idfWeightsMureDickieTest.txt", "tf-idfWeightsMureDickieTrain.txt",
				"tf-idfWeightsRobinSidelTest.txt", "tf-idfWeightsRobinSidelTrain.txt"]
	vectorMapByDirList = []
	
	directoryList = ["C50test/JoeOrtiz/", "C50train/JoeOrtiz/", 
					 "C50test/JonathanBirt/", "C50train/JonathanBirt/", 
					 "C50test/MarkBendeich/", "C50train/MarkBendeich/", 
					 "C50test/MureDickie/", "C50train/MureDickie/", 
					 "C50test/RobinSidel/", "C50train/RobinSidel/"]

	# Generate Vector tables from input files to analyse
	for fileDirIdx in range(len(fileWeightsByDirList)):
		vectorMapByDirList.append(VecorMap(fileWeightsByDirList[fileDirIdx]))
	authorVectors = VecorMap(authorVectorsFile)

	# Clear documentCosSims.txt
	open(docOutFile, "w").close()

	# Open to edit
	fp = open(docOutFile, "w")
	table1 = singleAuthorComparisons(directoryList, vectorMapByDirList)
	writeDocComparisons(fp, table1)
	table2 = singleAuthorComparisonsBetweenSubsets(directoryList, vectorMapByDirList)
	writeDocComparisons(fp, table2)
	table3 = comparisonOfDifferentAuthors(directoryList, vectorMapByDirList)
	writeDocComparisons(fp, table3)
	fp.close()

def comparisonOfDifferentAuthors(directoryList, vectorMapByDirList):
	print "Starting Comparison Of Different Authors: Test"
	cosSimList = []
	docCosSimTable = [[0 for x in range(5)] for x in range(20)]  
						 #Row=directory:directory, 
					 	 #Col[1]=simMax, Col[2]=simMin, Col[3]=simAvg, Col[4]=stdDev	
	# For each TEST directory
	for dirIdx in xrange(len(directoryList), 2):
	#	dirIdx = 0
		# For each vector in the directoryList[dirIdx] VectorMap
		for i in range(len(vectorMapByDirList[dirIdx].getPathKeys())):
			path1Key = vectorMapByDirList[dirIdx].getPathKeys()[i]
			j = i + 2

			# For each vector in directoryList[dirIdx] VectorMap
			while ((dirIdx + 2) < len(vectorMapByDirList)) and j < len(vectorMapByDirList[dirIdx + 2].getPathKeys()):
				path2Key = vectorMapByDirList[dirIdx + 2].getPathKeys()[j]

				vec1 = vectorMapByDirList[dirIdx].getVectorAt(path1Key)
				vec2 = vectorMapByDirList[dirIdx + 2].getVectorAt(path2Key)
				sim = computeCosSim(vec1, vec2)

				if sim >= 0:
					cosSimList.append(sim)
				j += 2
		# Find max, min, average, standard deviation
		docData = findData(cosSimList)
		print docData
		if ((dirIdx + 2) < len(vectorMapByDirList)):
			docCosSimTable[dirIdx][0] = directoryList[dirIdx] + ":" + directoryList[dirIdx + 2] + " "
			docCosSimTable[dirIdx][1] = docData.mx
			docCosSimTable[dirIdx][2] = docData.mn
			docCosSimTable[dirIdx][3] = docData.avg
			docCosSimTable[dirIdx][4] = docData.stdev
		del cosSimList[:]#cosSimList = [] # Clear list

	print "Starting Comparison Of Different Authors: Train"
	# For each TRAIN directory
	for dirIdx in xrange(1, len(directoryList), 2):
#	dirIdx = 1
		# For each vector in the directoryList[dirIdx] VectorMap
		for i in range(1, len(vectorMapByDirList[dirIdx].getPathKeys())):
			path1Key = vectorMapByDirList[dirIdx].getPathKeys()[i]
			j = i + 2

			# For each vector in directoryList[dirIdx] VectorMap
			while ((dirIdx + 2) < len(vectorMapByDirList)) and j < len(vectorMapByDirList[dirIdx + 2].getPathKeys()):
				path2Key = vectorMapByDirList[dirIdx + 2].getPathKeys()[j]

				vec1 = vectorMapByDirList[dirIdx].getVectorAt(path1Key)
				vec2 = vectorMapByDirList[dirIdx + 2].getVectorAt(path2Key)
				sim = computeCosSim(vec1, vec2)

				if sim >= 0:
					cosSimList.append(sim)
				j += 2
		# Find max, min, average, standard deviation
		docData = findData(cosSimList)
		print docData
		if ((dirIdx + 2) < len(vectorMapByDirList)):
			docCosSimTable[dirIdx][0] = directoryList[dirIdx] + ":" + directoryList[dirIdx + 2] + " "
			docCosSimTable[dirIdx][1] = docData.mx
			docCosSimTable[dirIdx][2] = docData.mn
			docCosSimTable[dirIdx][3] = docData.avg
			docCosSimTable[dirIdx][4] = docData.stdev
		del cosSimList[:]#cosSimList = [] # Clear list

	return docCosSimTable


def singleAuthorComparisonsBetweenSubsets(directoryList, vectorMapByDirList):
	print "Starting Single Author Comparisons Between Subsets"
	cosSimList = []
	docCosSimTable = [[0 for x in range(5)] for x in range(5)]  
						 #Row=directory:directory, 
					 	 #Col[1]=simMax, Col[2]=simMin, Col[3]=simAvg, Col[4]=stdDev	
	# For each directory
	for dirIdx in xrange(len(directoryList), 2): # Incrememnt by 2
#		dirIdx = 0		

		# For each vector in the directoryList[dirIdx] VectorMap
		for i in range(len(vectorMapByDirList[dirIdx].getPathKeys())):
			path1Key = vectorMapByDirList[dirIdx].getPathKeys()[i]

			# For each vector in directoryList[dirIdx] VectorMap
			for j in range(len(vectorMapByDirList[dirIdx + 1].getPathKeys())):
				path2Key = vectorMapByDirList[dirIdx + 1].getPathKeys()[j]

				vec1 = vectorMapByDirList[dirIdx].getVectorAt(path1Key)
				vec2 = vectorMapByDirList[dirIdx + 1].getVectorAt(path2Key)
				sim = computeCosSim(vec1, vec2)

				if sim >= 0:
					cosSimList.append(sim)
				j += 1

		# Find max, min, average, standard deviation
		docData = findData(cosSimList)
		print docData
		headerString = directoryList[dirIdx] + ":" + directoryList[dirIdx + 1] + " "
		docCosSimTable[dirIdx][0] = headerString
		docCosSimTable[dirIdx][1] = docData.mx
		docCosSimTable[dirIdx][2] = docData.mn
		docCosSimTable[dirIdx][3] = docData.avg
		docCosSimTable[dirIdx][4] = docData.stdev
		del cosSimList[:]#cosSimList = [] # Clear list

	return docCosSimTable

# Single Author Comparisons start with full file path
# Single Author Comparisons Between Subsets start with author's name
# Comparison of Different Authors start with author1:author2
#
def writeDocComparisons(fp, table):
	outString = ""
	columns = len(table[0])
	rows = len(table)
	for i in range(rows):
		for j in range(columns):
			outString += str(table[i][j]) + " "
		outString += "\n"
	fp.write(outString)

def singleAuthorComparisons(directoryList, vectorMapByDirList):
	print "Starting Single Author Comparisons"
	cosSimList = []
	docCosSimTable = [[0 for x in range(5)] for x in range(10)]  
						 #Row=directory, 
					 	 #Col[1]=simMax, Col[2]=simMin, Col[3]=simAvg, Col[4]=stdDev	
	# For each directory
	for dirIdx in range(len(directoryList)):
		# For each vector in the directoryList[dirIdx] VectorMap
#		dirIdx = 0
		for i in range(len(vectorMapByDirList[dirIdx].getPathKeys())):
			path1Key = vectorMapByDirList[dirIdx].getPathKeys()[i]
			j = i + 1
			# For each vector in directoryList[dirIdx] VectorMap
			while j < len(vectorMapByDirList[dirIdx].getPathKeys()):
				path2Key = vectorMapByDirList[dirIdx].getPathKeys()[j]
				vec1 = vectorMapByDirList[dirIdx].getVectorAt(path1Key)
				vec2 = vectorMapByDirList[dirIdx].getVectorAt(path2Key)
				sim = computeCosSim(vec1, vec2)
				if sim >= 0:
					cosSimList.append(sim)
				j += 1
		# Find max, min, average, standard deviation
		docData = findData(cosSimList)
		print docData
		docCosSimTable[dirIdx][0] = directoryList[dirIdx]
		docCosSimTable[dirIdx][1] = docData.mx
		docCosSimTable[dirIdx][2] = docData.mn
		docCosSimTable[dirIdx][3] = docData.avg
		docCosSimTable[dirIdx][4] = docData.stdev
		del cosSimList[:]#cosSimList = [] # Clear list

	return docCosSimTable

# Find max, min, average, standard deviation
# @param cosSimList - List of cos sims to evaulate
def findData(cosSimList):
	mx = 0.0
	mn = 1.0
	total = 0.0
	avg = 0.0
	stdev = 0.0
	# for all the value in our list
	for value in cosSimList:
		if value > mx:
			mx = value
		if value < mn:
			mn = value
		total += value
	if len(cosSimList) > 0:
		avg = total / len(cosSimList)
	stdev = np.std(np.array(cosSimList))
	docData = DocData(mx, mn, avg, stdev)
	return docData

# cos(x,y) =
# [sum(x * y)][sqrt(x^2) * sqrt(y^2)]
# Where sum(x * y) is the dot product of vectors x and y
def computeCosSim(vec1, vec2,):
	numerator = 0
	denominator1 = 0
	denominator2 = 0
	vec1ElemPointer = 0 # Element position
	vec2ElemPointer = 0 # Element position
	vec1Keys = vec1.keys() # List of vect1 keys
	vec2Keys = vec2.keys() # List of vect2 keys
	vect1Length = len(vec1Keys) # Number of elements in vec1
	vect2Length = len(vec2Keys) # Number of elements in vec2
	# While vec1 and vec2 have keys
	while vec1ElemPointer < vect1Length and vec2ElemPointer < vect2Length:
		# If vec1's key == vec2's key
		if vec1Keys[vec1ElemPointer] == vec2Keys[vec2ElemPointer]:
			# compute dot product
			numerator += vec1[vec1Keys[vec1ElemPointer]] * vec2[vec2Keys[vec2ElemPointer]]
			# compute vect1[elem]^2
			denominator1 += pow(vec1[vec1Keys[vec1ElemPointer]], 2)
			# compute vect2[elem]^2
			denominator2 += pow(vec2[vec2Keys[vec2ElemPointer]], 2)
			vec1ElemPointer += 1
			vec2ElemPointer += 1
		# If vec1's key > vect2's key
		elif vec1Keys[vec1ElemPointer] > vec2Keys[vec2ElemPointer]:
			# icrement vect2's key pointer
			vec2ElemPointer += 1
		# If vec1's key < vect2's key
		elif vec1Keys[vec1ElemPointer] < vec2Keys[vec2ElemPointer]:
			# icrement vect1's key pointer
			vec1ElemPointer += 1
	# Compute denominator
	denominator = sqrt(denominator1) * sqrt(denominator2)
	# Compute cos sim
	if (denominator > 0):
		return numerator / denominator
	else:
		return -1

main()


