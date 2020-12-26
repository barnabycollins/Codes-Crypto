import what3words
from w3w_apiKey import apiKey
from tqdm import tqdm
import re

gc = what3words.Geocoder(apiKey)

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
durham = what3words.Coordinates(54.4634, 1.3424)

results = {}

for i in tqdm(alphabet):
    for j in alphabet:
        address = f'tile.bil{i}.{j}'

        res = gc.autosuggest(address, focus=durham)

        for k in res['suggestions']:
            dist = k['distanceToFocusKm']
            addr = k['words']

            if (re.match(r'^tile\.bil[a-z\.]{8}$', addr)):
                print(addr)
                if (dist not in results):
                    results[dist] = set()

                results[dist].add(k)

import json

store = open('w3w_results.json', 'w')

json.dump(results, store)

store.close()
