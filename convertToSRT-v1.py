import re

#Cycle through each file in the folder

#Gets each line in file and create a tuple with timestamp, content, then add it to a list
#make sure to ignore header and blank lines

def getLines():
    file = open('test2.txt','r')

    timedLineList = []

    lineTime = 'XXXXXXXXXXXXXXXXXXXXXXX'
    lineText= 'XXXXXXXXXXXXXXXXXXXXXXX'

    #LineTimedText
    count = 0
    for line in file:
            timedLine = [0,0]
            line = line.strip()
            #print(line)
            #catches blank lines
            if re.findall(r'^\s*$', line):
                pass
            #    print(re.findall(r'^\s*$', line))
            #catches instances where timestamp and text are not on the same line
            elif re.findall(r'^[^\[][\w]+',line):
                lineText = str(re.findall(r'^[[\s|\w]+',line))
                lineText = lineText[2:-2].strip()
                #timedLineList.append(lineTime, lineText)
                #timedLineList[count] = lineTime, lineText

                count+=1
            elif re.findall(r'[0-9]+[\:][0-9]+[\:][0-9]+[\.][0-9]+', line):
                lineTime = str(re.findall(r'[0-9]+[\:][0-9]+[\:][0-9]+[\.][0-9]+', line))
                lineTime = lineTime[2:-2].strip()
                lineTime = lineTime
                lineText = str(re.findall(r'[\]][\s|\w]*', line))
                lineText = lineText[5:-2].strip()
                timedLineList[count] = lineTime, lineText
        #        timedLineList.append(lineTime, lineText)
                count+=1
            else:
                pass

    print(timedLineList)

    file.close()


getLines()
