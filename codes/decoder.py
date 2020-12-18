from utils import getFileFromCommand

(fileInfo, fileName) = getFileFromCommand()

inFile = open(fileName, 'r', newline='')

outFile = open(f'{fileInfo["name"]}-decoded.tex', 'w', newline='')

outFile.write(inFile.read())

inFile.close()
outFile.close()