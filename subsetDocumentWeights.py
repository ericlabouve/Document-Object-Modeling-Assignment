# Goal: parse tf-idfWeightsDocuments.txt into separate documents that contain
# file vectors weights for each author

def main():
	infile = "tf-idfWeightsDocuments.txt"
	outFiles = ["tf-idfWeightsJoeOrtizTest.txt", "tf-idfWeightsJoeOrtizTrain.txt", 
				"tf-idfWeightsJonathanBirtTest.txt", "tf-idfWeightsJonathanBirtTrain.txt", 
				"tf-idfWeightsMarkBendeichTest.txt", "tf-idfWeightsMarkBendeichTrain.txt",
				"tf-idfWeightsMureDickieTest.txt", "tf-idfWeightsMureDickieTrain.txt",
				"tf-idfWeightsRobinSidelTest.txt", "tf-idfWeightsRobinSidelTrain.txt"]
	directoryList = ["C50test/JoeOrtiz/", "C50train/JoeOrtiz/", 
					 "C50test/JonathanBirt/", "C50train/JonathanBirt/", 
					 "C50test/MarkBendeich/", "C50train/MarkBendeich/", 
					 "C50test/MureDickie/", "C50train/MureDickie/", 
					 "C50test/RobinSidel/", "C50train/RobinSidel/"]
	outFpList = [] # List of outFile pointers

	# Open infile for reading
	infp = open(infile, "r")

	# Clear all outFiles
	for outFileIdx in range(len(outFiles)):
		open(outFiles[outFileIdx]).close()

	# Open all outFiles for writing
	for outFileIdx in range(len(outFiles)):
		outFpList.append(open(outFiles[outFileIdx], "w"))
		outFpList[outFileIdx].write("path index weight\n")

	# Loop through each line in tf-idfWeightsDocuments.txt
	lineNum = 1
	for line in infp:
		if lineNum > 1:
			outFileIdx = getDirLoc(line, directoryList)
			outFpList[outFileIdx].write(line)
		else:
			lineNum += 1

	# Close all outFiles
	for fp in outFpList:
		fp.close()
		
	# Close our input read file
	infp.close()

# Given a line, returns corresponding file index in outFiles
def getDirLoc(line, directoryList):
	for dirIdx in range(len(directoryList)):
		if directoryList[dirIdx] in line:
			return dirIdx
	return 0

main()