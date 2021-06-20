import re

def getVariableList(text,start="{",end="}"):
    elem = []
    pattern = start + "(.*?)" + end
    for match in re.finditer(pattern, text):
        lenStart = len(start)
        lenEnd = len(end)
        sGroup = match.group()[lenStart:len(match.group())-lenEnd]
        print(sGroup)
        elem.append(sGroup)
    # Print match
    #print('Match "{}" found at: [{},{}]'.format(sGroup, sStart,sEnd))
    return elem

