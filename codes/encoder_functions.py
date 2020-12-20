
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

def lzw(inData, max_char=255):

    dictIndex = max_char+1

    encode_dict = {}
    for i in range(dictIndex):
        encode_dict[chr(i)] = i

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
    
    return outData

    
def huffman_and_lzw(inData):
    return huffman_test(lzw(inData))

def replace_runs(inData, expanded_chars=False):
    low_bound = 255
    if (expanded_chars):
        low_bound = 767

    replaced = ''

    max_char = low_bound

    i = 0
    while i < len(inData):
        j = i+1
        while (j < len(inData) and inData[j] == inData[i]):
            j += 1
        
        if (j-i > 3):
            charToAdd = low_bound + j-i
            replaced += inData[i] + chr(charToAdd)
            
            max_char = max(max_char, charToAdd)
        
        else:
            replaced += inData[i:j]

        i = j
    
    return (replaced, max_char)

def replace_tags(inData):
    import re
    from collections import Counter
    
    # regexes of (preferably mutually exclusive) common patterns (in this case, TeX tags)
    tagGroups = [
        r'(\\[a-zA-Z]+)',                       # standard TeX tag
        r'(\\[a-zA-Z]+(?:\{[a-zA-Z ]*\})+)',    # TeX tag with parameters following it
        r'[ \n]([a-zA-Z]+)[ \.,:;!]'            # words
    ]

    numGroups = len(tagGroups)

    tagGroups_scored = []
    for i in tagGroups:
        counts = Counter(re.findall(i, inData))

        tagGroups_scored.append(Counter())

        for tag in counts.keys():
            tagGroups_scored[-1][tag] = (len(tag)-1)*counts[tag]
            # compute score (this is the length of a tag minus the length of the character replacing it, times the number of instances of that tag)

    
    groupScores_cumulative = []
    for i in tagGroups_scored:
        groupScores_cumulative.append([])
        runningTotal = 0
        for j in i.most_common():
            runningTotal += j[1]
            groupScores_cumulative[-1].append(runningTotal)

    
    allocated_space = 512

    groupMaxes = [len(groupScores_cumulative[i]) for i in range(numGroups)]

    allocated_space = min(512, sum(groupMaxes))

    # generate initial, equal allocation
    allocation = [0]*numGroups
    for i in range(allocated_space):
        group = i%numGroups
        if (allocation[group] == groupMaxes[group]):
            i -= 1
            continue
        
        allocation[i%numGroups] += 1

    # optimise allocation
    lastTotal = sum([groupScores_cumulative[i][allocation[i]-1] for i in range(numGroups) ])

    # do-while loop
    while True:
        potentialLosses = [groupScores_cumulative[i][allocation[i]-1]-groupScores_cumulative[i][allocation[i]-2] for i in range(numGroups)]
        toLoseOne = potentialLosses.index(min(potentialLosses))

        potentialGains = [groupScores_cumulative[i][allocation[i]]-groupScores_cumulative[i][allocation[i]-1] if (allocation[i] < groupMaxes[i]) else 0 for i in range(numGroups)]
        toGainOne = potentialGains.index(max(potentialGains))

        if (toGainOne != toLoseOne):
            allocation[toGainOne] += 1
            allocation[toLoseOne] -= 1

        newTotal = sum([groupScores_cumulative[i][allocation[i]-1] for i in range(numGroups)])

        if (newTotal <= lastTotal):
            break
        
        lastTotal = newTotal

    translation_table = {}
    for i in range(numGroups):
        replacements = tagGroups_scored[i].most_common(allocation[i])
        for j in range(allocation[i]):
            character = chr(256 + sum(allocation[:i]) + j)
            inData = inData.replace(replacements[j][0], character)
            translation_table[character] = replacements[j][0]
    
    return (inData, translation_table)

def replace_repeats_then_lzw(inData):
    import pickle

    (noRuns, max_char) = replace_runs(inData, True)

    (replacedTags, dictionary) = replace_tags(noRuns)

    compressed = lzw(replacedTags, max_char)

    return pickle.dumps((max_char, dictionary, compressed), protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':

    replace_repeats_then_lzw(open('testdocs/test1.tex', 'r', newline='').read())

    #import decoder_functions
