import json

def dictGetDataByKey(dictData, key):
    if hasKey(dictData, key):
        return dictData[key]
    return None

def hasKey(dictData, key):
    for k in dictData:
        if k == key:
            return True
    return False

def writeJson(filename, jsonData, mode = "w"):
    print("Writing Json:" + filename)

    with open(filename, mode,  encoding = 'utf-8') as file_obj:
        json.dump(jsonData, file_obj, ensure_ascii=False)
    print("Finish Writing!")

def readAsJson(filename):
    with open(filename, 'r',  encoding = 'utf-8') as file_obj:
        jsonData = json.load(file_obj)
    return jsonData

token = None
def getGitToken():
    global token
    if (token != None):
        return token

    with open(r"../token.txt", 'r') as file_obj:
        token = file_obj.readline()
    return token

token_micode = None
def getGitTokenMicode():
    global token_micode
    if (token_micode != None):
        return token_micode

    with open(r"../token_micode.txt", 'r') as file_obj:
        token_micode = file_obj.readline()
    return token_micode
