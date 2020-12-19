from collections import Counter
from utils import getFileFromCommand
import re

(fileInfo, fileName) = getFileFromCommand()

contents = open(fileName, 'r').read()

instanceLength = 1
instances = re.findall(".{" + str(instanceLength) + "}", contents)

counts = Counter(instances)

counts_sorted = sorted(list(dict(counts).items()), key=lambda x: x[1])

maxCount = counts_sorted[-1][1]

for i in counts_sorted[-1000:]:
    print("{:24} {:6} {}".format(repr(i[0]), i[1], '#'*round(128*i[1]/maxCount)))
