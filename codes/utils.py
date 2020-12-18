import sys, re

pythonCommand = 'python374'

def getFileFromCommand():

    if (len(sys.argv) == 2):
        match = re.match(r"(.*)\.(tex|lz)", sys.argv[1])
        
        if (match != None):
            (name, extension) = match.groups()
            return ({
                'name': name,
                'extension': extension
            }, sys.argv[1])
    
    raise Exception(f'Incorrect number of arguments detected! Expected 2, received {len(sys.argv)}')