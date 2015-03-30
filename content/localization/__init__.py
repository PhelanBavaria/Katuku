

import os
import yaml



DEFAULT = 'ENG'
set_lang = 'ENG'


localizations = {}

for lang in os.listdir('content/localization'):
    if '__' in lang:
        continue
    localizations[lang] = {}
    for local in os.listdir('content/localization/' + lang):
        raw = open('content/localization/' + lang + '/' + local).read()
        content = yaml.load(raw)
        localizations[lang].update(content)

def translate(tag, lang=set_lang):
    try:
        trans = localizations[set_lang][tag]
    except KeyError:
        try:
            trans = localizations[DEFAULT][tag]
        except KeyError:
            return ''
    return trans
