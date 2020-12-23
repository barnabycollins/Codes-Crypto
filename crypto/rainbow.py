from subprocess import check_output
from tqdm import tqdm

import json

import multiprocessing as mp

dictionary = json.load(open('words_dictionary.json'))

filteredByLength = [[] for i in range(13)]

for i in dictionary.keys():
    l = len(i)

    if (l == 4):
        filteredByLength[l].append(i)

del dictionary

for i in filteredByLength:
    print(len(i))

import json

possibleStrings = []
for i in range(4, 13):
    for j in range(4, 12-i):
        k = 12-i-j
        print(f'Working on {i}, {j}, {k}...')
        for word1 in tqdm(filteredByLength[i]):
            for word2 in filteredByLength[j]:
                for word3 in filteredByLength[k]:
                    possibleStrings.append(f'{word1}.{word2}.{word3}')

        json.dump(possibleStrings, open('all3words.json', 'w'))

print(possibleStrings[:100])



target = b'903408ec4d951acfaeb47ca88390c475'
targets = [target[i:i+16] for i in range(int(len(target)/16))]

def encrypt(input):
    return check_output(f"encrypt.exe {input}")

rainbowTable = {}

print(rainbowTable)
