import json

dictionaryFile = '/var/www/html/web-control/src/plugins/dictionary-plugin/dictionary.json'

with open(dictionaryFile) as json_file:
    data = json.load(json_file)
    for p in data['measurements']:
        print(p['name'] + ':\t\t' + p['key'])
