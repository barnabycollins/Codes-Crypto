from collections import Counter
from utils import getFileFromCommand

(fileInfo, fileName) = getFileFromCommand()

contents = open(fileName, 'r').read()

counts = Counter(contents)

counts_sorted = sorted(list(dict(counts).items()), key=lambda x: x[1])

maxLength = counts_sorted[-1][1]

for i in counts_sorted:
    print("{:4} {:6} {}".format(repr(i[0]), i[1], '#'*round(128*i[1]/maxLength)))