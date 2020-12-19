
def passthrough(inData):
    return inData

def huffman_test(inData):
    from dahuffman import HuffmanCodec
    import pickle
    
    codec = HuffmanCodec.from_data(inData)

    table = codec.get_code_table()

    encoded = codec.encode(inData)

    to_pickle = (table, encoded)

    return pickle.dumps(to_pickle, protocol=pickle.HIGHEST_PROTOCOL)

def lzw(inData):
    import pickle # TODO see if you can come up with a better way

    encode_dict = {}
    for i in range(256):
        encode_dict[chr(i)] = i
    
    dictIndex = 256

    outData = []

    i = 0
    while i < len(inData):
        j = i+1
        
        while inData[i:j] in encode_dict and j <= len(inData):
            j += 1


        outData.append(encode_dict[inData[i:j-1]])

        encode_dict[inData[i:j]] = dictIndex

        dictIndex += 1

        i = j-1
    
    return pickle.dumps(outData, protocol=pickle.HIGHEST_PROTOCOL)

'''
import decoder_functions

print(decoder_functions.lzw(lzw('DDDDDDD')))
'''