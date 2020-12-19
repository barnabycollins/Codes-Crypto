from utils import getFileFromCommand
import decoder_functions

(fileInfo, fileName) = getFileFromCommand()

inFile = open(fileName, 'rb')
inData = inFile.read()
inFile.close()

functionToUse = decoder_functions.lzw

outData = functionToUse(inData)

outFile = open(f'{fileInfo["name"]}-decoded.tex', 'w', newline='')
outFile.write(outData)
outFile.close()