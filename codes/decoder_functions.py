
def passthrough(inData):
    return inData

def huffman_test(inData):
    from dahuffman import HuffmanCodec
    import pickle
    from functools import reduce

    (table, encoded) = pickle.loads(inData)
    
    codec = HuffmanCodec(table)

    decoded = codec.decode(encoded)

    return reduce(lambda x,y: x+y, decoded)

def lzw(inData, max_char=255):
    dictIndex = max_char+1 # add one to include max_char itself in ranges

    decode_dict = {}
    for i in range(dictIndex):
        decode_dict[i] = chr(i)

    outData = lastStep = decode_dict[inData[0]]

    for i in range(1, len(inData)):

        try:
            thisStep = decode_dict[inData[i]]
        
        except:
            thisStep = lastStep + lastStep[0]
        
        decode_dict[dictIndex] = lastStep + thisStep[0]

        outData += thisStep

        lastStep = thisStep
        
        dictIndex += 1

    return outData

def replace_tags(inData, dictionary):
    for i in dictionary.keys():
        inData = inData.replace(i, dictionary[i])
    
    return inData

def replace_runs(inData, expanded_chars = False):
    replaced = ''
    bound = len(inData)

    low_char_bound = 767 if expanded_chars else 255

    i = 0
    while i < bound:
        char = inData[i]
        
        if (i < bound-1 and ord(inData[i+1]) > low_char_bound):
            replaced += char * (ord(inData[i+1]) - low_char_bound)

            i += 2
        
        else:
            replaced += char

            i += 1
    
    return replaced

def replace_repeats_then_lzw(inData):
    import pickle

    (max_char, dictionary, compressed) = pickle.loads(inData)

    replacedTags = lzw(compressed, max_char)

    noRuns = replace_tags(replacedTags, dictionary)

    return replace_runs(noRuns, True)


def huffman_and_lzw(inData):
    return lzw(huffman_test(inData))
