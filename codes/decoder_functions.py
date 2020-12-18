
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