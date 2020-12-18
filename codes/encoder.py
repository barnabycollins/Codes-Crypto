from utils import getFileFromCommand

(fileInfo, fileName) = getFileFromCommand()

inFile = open(fileName, 'r')

outFile = open(f'{fileInfo["name"]}.lz', 'w', newline='\n')

outFile.write(inFile.read())

inFile.close()
outFile.close()