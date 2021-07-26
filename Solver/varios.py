import re

def getVariableList(text,start="{",end="}"):
    try:
        elem = []
        pattern = start + "(.*?)" + end
        for match in re.finditer(pattern, text):
            lenStart = len(start)
            lenEnd = len(end)
            sGroup = match.group()[lenStart:len(match.group())-lenEnd]
            elem.append(sGroup)
        #print('Match "{}" found at: [{},{}]'.format(sGroup, sStart,sEnd))
        return elem
    except Exception as error:
        print("Error al obtener la lista de variables de la formula..",error)


