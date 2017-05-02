import os
from os.path import join, getsize
import json
import re

def listTextTracks(theDir):
    a = {}
    for root, dirs, files in os.walk(theDir):
        for name in files:
            if re.search('DS_Store',os.path.join(root, name)):
                pass
            else:
                a['fullpath'] = os.path.join(root, name)
                a['name']=name
                newname = 'fileNameList.json'
                with open(newname,'a') as fp:
                    json.dump(a, fp)
                    fp.write("\n")
        fp.close()
    return newname

if __name__ == "__main__":
    theDir = 'text_tracks'
    listTextTracks(theDir)
