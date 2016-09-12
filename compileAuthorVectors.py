def main():
	authorVectorFileNames = ["JoeOrtizVectors.txt", "JonathanBirtVectors.txt", "MarkBendeichVectors.txt", "MureDickieVectors.txt", "RobinSidelVectors.txt"]
	outFile = "tf-idfWeightsAuthors.txt"
	outFilep = open(outFile, "w")
	outFilep.write("path index:weight")
	for authorFile in authorVectorFileNames:
		filep = open(authorFile, "r")
		contents = filep.read()
		outFilep.write(contents)
		filep.close()
	outFilep.close()

main()
