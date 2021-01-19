from utils import getFileFromCommand
import encoder_functions

# Get file information from the CLI
(fileInfo, fileName) = getFileFromCommand()

# Read file
inFile = open(fileName, 'r', newline='')
inData = inFile.read()
inFile.close()

# Apply compression
functionToUse = encoder_functions.replace_repeats_then_lzw
outData = functionToUse(inData)

# Write output
outFile = open(f'{fileInfo["name"]}.lz', 'wb')
outFile.write(outData)
outFile.close()