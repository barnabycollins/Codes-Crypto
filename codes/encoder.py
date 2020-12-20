from utils import getFileFromCommand
import encoder_functions

(fileInfo, fileName) = getFileFromCommand()

inFile = open(fileName, 'r', newline='')
inData = inFile.read()
inFile.close()

functionToUse = encoder_functions.replace_repeats_then_lzw

outData = functionToUse(inData)

outFile = open(f'{fileInfo["name"]}.lz', 'wb')
outFile.write(outData)
outFile.close()