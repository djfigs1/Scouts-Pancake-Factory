import json

def getConfigSetting(setting):
    with open('config.json') as f:
        js = json.load(f)
        result = None
        try:
            result = js[setting]
        except KeyError:
            result = ""
        return result
