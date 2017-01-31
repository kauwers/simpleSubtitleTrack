import re

#Cycle through each file in the folder

#Gets each line in file and create a tuple with timestamp, content, then add it to a list
#make sure to ignore header and blank lines

def getLines():
    file = open('test2.txt','r')

    textLines = []
    lineNumber = 1
    lineTime = 'XXXXXXXXXXXXXXXXXXXXXXX'
    lineText= 'XXXXXXXXXXXXXXXXXXXXXXX'

    #LineTimedText

    for line in file:
            line = line.strip()
        #    print(line)
            #catches blank lines
            if re.findall(r'^\s*$', line):
                pass
            #    print(re.findall(r'^\s*$', line))
            #catches instances where timestamp and text are not on the same line
            elif re.findall(r'^[^\[][\w]+',line):
                lineText = str(re.findall(r'^[[\s|\w]+',line))
                lineText = lineText[2:-2].strip()
                timedLine = lineTime, lineText
            elif re.findall(r'[0-9]+[\:][0-9]+[\:][0-9]+[\.][0-9]+', line):
                lineTime = str(re.findall(r'[0-9]+[\:][0-9]+[\:][0-9]+[\.][0-9]+', line))
                lineTime = lineTime[2:-2].strip()
                lineTime = lineTime
                lineText = str(re.findall(r'[\]][\s|\w]*', line))
                lineText = lineText[5:-2].strip()
                timedLine = lineTime, lineText
            print(timedLine)




    file.close()


getLines()
