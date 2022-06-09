import sys
import argparse
import json
import time
from googletrans import Translator
import os

# from pymysql import NULL


def findAllTranslateFiles(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                language = os.path.basename(file).replace('.json', '')
                if 'zh_CN' == language:
                    language = 'zh-CN'
                obj = {
                    'path': os.path.join(root, file),
                    'language': language
                }
                yield obj


def do_translate(json_path, src_language, dest_language, key, content, translator):
    # dict = NULL
    with open(json_path, 'r+') as load_from:
        dict = json.load(load_from)
        if key in dict:
            print('key exist, skip!!!')
        elif dest_language == src_language:
            print('same language, skip!!!')
            dict[key] = content
        else:
            result = translator.translate(
                content, dest=dest_language, src=src_language)
            dict[key] = result.text
    with open(json_path, 'w+') as f:
        json.dump(dict, f, ensure_ascii=False)
    time.sleep(0.5)


def do_translate_files(translate_files, src_language, key, content):
    translator = Translator()
    for translate_file in translate_files:
        print('path = ' + translate_file['path'])
        print('language = ' + translate_file['language'])
        print('*'*20)
        # do translate by language
        do_translate(json_path=translate_file['path'], src_language=src_language,
                     dest_language=translate_file['language'], key=key, content=content, translator=translator)


def run(project_path):
    print('=============START=============')
    try:
        print('project_path = ' + project_path)
        # find the language files
        root = project_path + '/resources/lang/'
        translate_files = findAllTranslateFiles(root)
        # do translate
        with open('data.json', 'r') as load_from:
            dict = json.load(load_from)
            do_translate_files(translate_files, dict['language'], dict['key'], dict['content'])
    except Exception as e:
        print('cause expection!!')
        print(e)
    print('==============END==============')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--perform',
        action='store_true',
        help='Perform and run commands',
        required=True)
    parser.add_argument(
        '--project_path', help='Laravel project root path', required=True)
    args = parser.parse_args()
    run(project_path=args.project_path)


if __name__ == '__main__':
    sys.exit(main())
