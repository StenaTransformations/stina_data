import json
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.realpath(os.path.join(BASE_DIR, 'data'))


def parse_corpus(file_path, corpus=None):
    if corpus is None:
        corpus = {}

    with open(file_path, 'r') as f:
        for line in f:
            s = line.split(',')
            if len(s) < 2:
                continue
            category, entity, gazette = s[0], s[1].strip(), []
            if len(s) > 2:
                gazette = [w.strip() for w in s[2:]]

            if category in corpus:
                corpus[category].append({entity: [entity] + gazette})
            else:
                corpus[category] = [{entity: [entity] + gazette}]
        return corpus


def write_to_file(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)


def convert_text_files():
    """Convert text files to JSON"""
    for lang_dir in os.listdir(DATA_DIR):
        dir_path = os.path.join(DATA_DIR, lang_dir)
        print(f'Checking {dir_path}')

        for fname in os.listdir(dir_path):
            if fname.startswith('.'):
                continue

            file_path = os.path.join(dir_path, fname)
            base_path, ext = os.path.splitext(file_path)

            if ext != '.txt':
                continue

            print(f'Found file {fname}')

            try:
                data = parse_corpus(file_path)
                print(f'Parsed file {fname}')
                new_file = f'{base_path}.json'
                print(f'Creating new file {new_file}')
                write_to_file(new_file, data)
                print()
            except Exception as e:
                print('Error parsing file {}: {}'.format(file_path, e))
                continue


if __name__ == '__main__':
    convert_text_files()
