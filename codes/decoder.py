from utils import getFileFromCommand
import decoder_functions

# Get file information from the CLI
(fileInfo, fileName) = getFileFromCommand()

# Read file
inFile = open(fileName, 'rb')
inData = inFile.read()
inFile.close()

# Apply compression
functionToUse = decoder_functions.replace_repeats_then_lzw
outData = functionToUse(inData)

# Write output
outFile = open(f'{fileInfo["name"]}-decoded.tex', 'w', newline='')
outFile.write(outData)
outFile.close()