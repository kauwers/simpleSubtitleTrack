import re
import json
from fileNameList import listTextTracks
import os

#for input - Gets each line in file and create a tuple with timestamp, content, then add them to a dictionary as strings {timestamp, text}
def getTimedLines(filePath):
    file = open(filePath,'r')
    timedLineDict = {}
    lineTime, lineText, timedLine = 'XXXXXXXXXXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXXXXXXXXXX'
    count = 0
    for line in file:
        line = line.strip()
        line = removeTabs(line)
        #catches QT code brackets and removes them - sometimes these are on the same line as actual timestamps
        if re.search(r'[\{]', line):
            #brackets = re.findall(r'[\{].*[\}]',line)
            line = re.sub(r'[\{].*[\}]', "", line)
        #catches blank lines
        if re.findall(r'^\s*$', line):
            pass
        #catches other instances where timestamp and text are not on the same line
        elif re.findall(r'^[^\[][\w]+',line):
            lineText = removeBadQuotes(str(re.findall(r'^[[\s|\S]+',line)))
            lineText = lineText[2:-2].strip()
            addToTimedLine(lineTime, lineText , timedLineDict)
        #catch instances where timestamp and text are on the same line
        elif re.findall(r'[0-9]+[\:][0-9]+[\:][0-9]+[\.][0-9]+', line):
            lineTime = findTimeStamp(line)
            lineTime = lineTime[2:-2].strip()+'5'
            lineText = removeBadQuotes(str(re.findall(r'[\]][\s|\S]*', line)))
            lineText = lineText[3:-2].strip()
            addToTimedLine(lineTime, lineText, timedLineDict)
        else:
            pass
    file.close()
    return timedLineDict

#for input - adds each line to the dictionary{string : string}, combines blank lines and lines with text but no timestamp, and instances where timestamp and text are not on the same line because there are two speakers onto a single line
def addToTimedLine(time, text, theDict):
    #check for completely blank lines and replace with a space - Kaltura SRT reader requires at least one space per line.
    if re.search(r'^\s*$',text):
        text = " "
    #add time and lines, that have not already been added
    if time not in theDict:
        theDict[time] = text
    #finds blank lines
    elif not re.search('[^\W]',theDict[time]):
        theDict[time] = text
    else:
        theDict[time] = theDict[time].strip()
        theDict[time] = theDict[time] + " " + text
    return theDict

#for input formatting - remove tabs
def removeTabs(line):
    line=str(re.sub('\t|\r|\n', ' ', line)) #remove tabs from lines
    return line
#for input formatting - fix for single quotes that occur between double quotes
def removeBadQuotes(line):
    line=str(re.sub(r"\\","", line))
    return line

#locates a string matching 00:00:00.00
def findTimeStamp(line):
    time=str(re.findall(r'[0-9]+[\:][0-9]+[\:][0-9]+[\.][0-9]+', line))
    time=str(re.sub(r'\.',',',time))
    return time

#format the dictionary as SRT
def writeTimedLines(lineDict, filename):
    #open writefile and add SRT to the name before the extension
    file = open(filename,'w')
    #splits lines with two speakers onto two lines
    for key in lineDict:
        name = re.findall(r'[A-Z][a-z]*[:]', lineDict[key])
        if len(name)==2:
            newline = lineDict[key].replace(name[1],'\n'+name[1])
            lineDict[key] = newline
    srtList=[]
    txtList = list(lineDict.keys())
    count = 1
    while count < len(txtList):
        srtList.append([txtList[count-1]+" --> "+txtList[count]])
        count+=1
    count = 1
    for k in lineDict:
        try:
            srtValue = str(srtList[count-1])
            srtValue = srtValue[2:-2]
            file.write(str(count-1)+'\n'+srtValue+'\n'+str(lineDict[k])+'\n\n')
            count+=1
        except:
            pass
    file.close()

#Cycle through each file in the folder
with open('fileNameList.json', 'r') as json_file:
#with open(theDir+listOfFiles, 'r') as json_file:
    theDir = 'text_tracks'
    os.mkdir("srt")
    for line in json_file:
        json_path = json.loads(line)
        oldPath = json_path['fullpath']
        newPath = oldPath.replace("txt", "srt")
        newPath = newPath.replace("text_tracks", "srt")
        theDict = getTimedLines(oldPath)
        writeTimedLines(theDict, newPath)
    json_file.close()
