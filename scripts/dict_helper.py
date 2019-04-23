import json

def state_from_openmct_dict(f=False):
    if not f:
        dictionaryFile = '/var/www/html/web-control/src/plugins/dictionary-plugin/dictionary.json'
    else:
        dictionaryFile = f
    dictionary = {}

    with open(dictionaryFile) as json_file:
        data = json.load(json_file)
        for p in data['measurements']:
            dictionary[p['key']]=0
    return dictionary
