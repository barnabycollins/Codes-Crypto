def findRepeatedSubstrings(inString):
    maxLength = 16
    stringDicts = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]

    for i in range(1, maxLength+1):
        for j in range(len(inString)-i):
            currentSubstring = inString[j:j+i]
            if (currentSubstring in stringDicts[i-1]):
                stringDicts[i-1][currentSubstring] += 1
            
            else:
                stringDicts[i-1][currentSubstring] = 1
        
        #print(f'Counted all items of length {i}!')

    for i in range(maxLength):
        
        for j in list(stringDicts[i].keys()):
            if (stringDicts[i][j] < 2):
                stringDicts[i].pop(j)
                continue
            
            if (i+1 != len(stringDicts)):
                for k in stringDicts[i+1].keys():
                    
                    if (j in k and stringDicts[i][j]*(i) < stringDicts[i+1][k]*(i+1)):
                            stringDicts[i].pop(j)
                            break
        
        #print(f'Up-filtered all items of length {i+1}!')

    for i in reversed(range(maxLength)):
        for j in list(stringDicts[i].keys()):
            for k in stringDicts[i-1].keys():
                if (k in j and stringDicts[i][j]*(i) > stringDicts[i-1][k]*(i-1)):
                        stringDicts[i].pop(j)
                        break

    
    return stringDicts

def replaceCommonSubstrings(inData):
    import threading, time, math

    from tqdm import tqdm
    
    num_threads = 16

    len_section = math.floor(len(inData)/num_threads)

    stringSections = [inData[i*len_section:(i+1)*len_section] for i in range(num_threads)]

    import multiprocessing as mp

    threads = mp.Pool(num_threads)
    results = threads.map(findRepeatedSubstrings, stringSections)

    finalDict = {}
    for i in results:
        for j in i[4:]:
            for k in j.keys():
                count = j[k]
                
                if (count < 10):
                    continue

                if (k in finalDict):
                    finalDict[k] += j[k]
                
                else:
                    finalDict[k] = j[k]

    finalDict = sorted(list(finalDict.items()), key=lambda x: x[1])
    print(finalDict[-100:])
        

    '''
    class stringCountThread(threading.Thread):
        def __init__(self, threadID, section):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.section = section
            self.result = []
        
        def run(self):
            print(f'Thread {self.threadID} beginning.')
            self.result = findRepeatedSubstrings(self.section)
            print(f'Thread {self.threadID} completed! :D')
        
        def return_result(self):
            return self.result

    threads = []

    for i in range(num_threads):
        threads.append(stringCountThread(i, stringSections[i]))
        threads[i].start()
    
    while threading.active_count() > 1:
        time.sleep(10)
    
    print("All work completed.")

    allDicts = []
    for i in range(num_threads):
        allDicts.append(threads[i].return_result())
    '''

    #bigStringDicts = findRepeatedSubstrings(inData)

    
if __name__ == '__main__':
    replaceCommonSubstrings(open('testdocs/test1.tex', 'r', newline='').read())