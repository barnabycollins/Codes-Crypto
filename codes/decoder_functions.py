
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

def lzw(inData):
    import pickle
    
    inData = list(pickle.loads(inData))

    decode_dict = {}
    for i in range(256):
        decode_dict[i] = chr(i)
    
    dictIndex = 256

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


