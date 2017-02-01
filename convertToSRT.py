import re

#Cycle through each file in the folder

#for input - Gets each line in file and create a tuple with timestamp, content, then add them to a dictionary as strings {timestamp, text}
def getTimedLines():
    file = open('test3.txt','r')
    timedLineDict = {}
    lineTime, lineText, timedLine = 'XXXXXXXXXXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXXXXXXXXXX'
    count = 0
    for line in file:
            line = line.strip()
            line = removeTabs(line)
            #catches blank lines and {}
            if re.findall(r'^\s*$|[\{]', line):
                pass
            #catches other instances where timestamp and text are not on the same line
            elif re.findall(r'^[^\[][\w]+',line):
                lineText = str(re.findall(r'^[[\s|\S]+',line))
                lineText = lineText[2:-2].strip()
                addToTimedLine(lineTime, lineText, timedLineDict)
            #catch instances where timestamp and text are on the same line
            elif re.findall(r'[0-9]+[\:][0-9]+[\:][0-9]+[\.][0-9]+', line):
                lineTime = findTimeStamp(line)
                lineTime = lineTime[2:-2].strip()

                lineText = str(re.findall(r'[\]][\s|\S]*', line))
                lineText = lineText[3:-2].strip()

                addToTimedLine(lineTime, lineText, timedLineDict)
            else:
                pass
    file.close()
    return timedLineDict

#for input - adds each line to the dictionary{string : string}, combines blank lines and lines with text but no timestamp, and instances where timestamp and text are not on the same line because there are two speakers onto a single line
def addToTimedLine(time, text, theDict):
    if time not in theDict:
        theDict[time] = text
    #finds blank lines
    elif not re.search('[^\W]',theDict[time]):
        theDict[time] = text
    else:
        theDict[time] = theDict[time].strip()
        theDict[time] = theDict[time] + " " + text
    return theDict

def removeTabs(line):
    line=str(re.sub('\t|\r|\n', ' ', line)) #remove tabs from lines
    return line

#locates a string matching 00:00:00.00
def findTimeStamp(line):
    time=str(re.findall(r'[0-9]+[\:][0-9]+[\:][0-9]+[\.][0-9]+', line))
    return time

theDict = getTimedLines()
for a in theDict:
    print(a+"      "+theDict[a])

#for output - creates a new line every time there is a timestamp that starts with a capital letter

#correct issue with single quotes formatting weird - maybe convert file format





#rewrite idea - use timestamp as a trigger and start a new list item after, otherwise build a string  On export, split lines by searching for single words that begin with a capital letter followed by a colon to split out speaker lines.
