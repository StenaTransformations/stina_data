import json
import os

def parse_corpus(filename, corpus={}):
    with open('data/{}'.format(filename), 'r') as f:
        for line in f.readlines():
            s = line.split(',')
            if len(s) < 2:
                continue
            category, entity, gazette = s[0], s[1].strip(), ([w.strip() for w in s[2:]] if len(s) > 2 else [])

            if category in corpus:
                corpus[category] = corpus[category] + [{entity:[entity] + gazette}]
            else:
                corpus[category] = [{entity:[entity] + gazette}]
        return corpus


def write_to_file(filename, data):
    with open('data/{}'.format(filename), 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)


valid = lambda x: x[0] != '.' and x.split('.')[1] == 'txt'


for file in list(filter(valid, os.listdir('data'))):
    try:
        print('\nfound file {} in data.'.format(file))
        data = parse_corpus(file)
        print('{} parsed.'.format(file))
        new_file = file.split('.')[0]+'.json'
        print('creating new file {}.'.format(new_file))
        write_to_file(new_file, data)
    except Exception as e:
        print('error parsing file {}: {}'.format(file, e))
        continue

