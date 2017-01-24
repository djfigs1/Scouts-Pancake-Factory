import json

def getConfigSetting(setting):
    js = getConfigJSON()
    try:
        result = js[setting]
    except KeyError:
        result = ""
    return result

def getConfigJSON():
    with open('config.json', 'r') as f:
        js = json.load(f)
        return js

def writeConfigSetting(setting, value):
    js = getConfigJSON()
    with open('config.json', 'w') as f:
        js[setting] = value
        json.dump(js, f)