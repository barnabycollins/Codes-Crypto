from subprocess import check_output

import multiprocessing as mp

target = b'903408ec4d951acfaeb47ca88390c475'
[target1, target2] = [target[i:i+16] for i in range(int(len(target)/16))]

def encrypt(input):
    return check_output(f"C:/encrypt.exe {input.encode(encoding='ascii').hex()}").strip()


def checkItem(item):
    global target1

    if (encrypt(item) == target1):
        return item

def genSegments(dump=True):
    from tqdm import tqdm
    import json

    dictionary = json.load(open('words_dictionary.json'))

    filteredByLength = dict((i, []) for i in [4, 5, 6])

    for i in dictionary.keys():
        l = len(i)

        if (4 <= l and l <= 6):
            filteredByLength[l].append(i)

    del dictionary

    possibleLengths = [
        [4, 4, 6],
        [4, 6, 4],
        [6, 4, 4],
        [4, 5, 5],
        [5, 4, 5],
        [5, 5, 4]
    ]

    numCharsInMiddle = [7 - i[0] for i in possibleLengths]

    requiredSplits = dict((i, set()) for i in [4, 5, 6])
    for i in range(len(possibleLengths)):
        requiredSplits[possibleLengths[i][1]].add(numCharsInMiddle[i])

    splits = dict((i, dict((j, [set(), set()]) for j in requiredSplits[i])) for i in [4, 5, 6])

    for i in splits:
        for j in splits[i]:
            for k in filteredByLength[i]:
                splits[i][j][0].add(k[:j])
                splits[i][j][1].add(k[j:])

    possibleSegments = [set(), set()]

    for [word1Length, word2Length, word3Length] in possibleLengths:
        print(f'\nStarting {word1Length}, {word2Length}, {word3Length}...')

        word2Half1Length = 7-word1Length

        for word1 in tqdm(filteredByLength[word1Length]):
            for halfWord2 in splits[word2Length][word2Half1Length][0]:
                possibleSegments[0].add(word1 + '.' + halfWord2)
        
        for halfWord2 in tqdm(splits[word2Length][word2Half1Length][1]):
            for word3 in filteredByLength[word3Length]:
                possibleSegments[1].add(halfWord2 + '.' + word3)

    if(dump):
        import pickle

        print('Writing file...')
        f = open('possibleSegments.pickle', 'wb')
        pickle.dump(possibleSegments, f, protocol=pickle.HIGHEST_PROTOCOL)
        f.close()
        
    return possibleSegments

def loadSegments():
    import pickle

    print('Loading segment file...')
    f = open('C:/possibleSegments.pickle', 'rb')
    possibleSegments = pickle.load(f)
    f.close()

    return possibleSegments



if (__name__ == '__main__'):
    import time, pickle

    possibleSegments = genSegments()
    possibleSegments = loadSegments()

    pool = mp.Pool(16)


    store = open('rainbowTable.pickle', 'rb')

    alreadyCompleted = pickle.load(store)

    print(f'Loaded {len(alreadyCompleted)} existing tuples.')

    store.close()


    to_process = list(possibleSegments[0].difference(alreadyCompleted))[:700000]
    
    print(f'Processing {to_process} items ({len(possibleSegments[0])} - {len(alreadyCompleted)})')

    del possibleSegments

    count = 0

    print(f'Generating table.')

    start = time.time()

    results = pool.imap_unordered(checkItem, to_process)

    found = False

    for i in results:
        if (count%256 == 0):
            print(f'{count}')

        if (i != None):
            print(f'FOUND IT: {i}')
            found = i
        
        count += 1
    
    end = time.time()

    pool.close()


    print(f'Total time taken: {end - start}')

    print('Finished. Storing results to disk...')


    import json
    
    store_js = open('rainbowtable.json', 'w')

    json.dump(list(alreadyCompleted | set(to_process)), store_js)

    store_js.close()


    store = open('rainbowTable.pickle', 'wb')

    pickle.dump(alreadyCompleted | set(to_process), store)

    store.close()

    print('Bam.')

    if (found):
        print(f'ALSO OMG WE FOUND IT, CHECK IT BROTHER:\n{found}')
