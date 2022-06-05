import requests
import os
import argparse
import json


def make_request(target_lang: str, text: str) -> requests.Response:
    body = {
        'targetLanguageCode': target_lang,
        'texts': text,
        # ниже вставляем id директории yandex cloud на место os.environ.get('translator_catalog_id')
        # либо же создаем соответствующую переменную окружения
        'folderId': os.environ.get('translator_catalog_id')
    }

    headers = {
        "Content-Type": "application/json",
        # ниже вставляем IAM токен yandex cloud на место os.environ.get('translator_catalog_id')
        # либо же создаем соответствующую переменную окружения
        "Authorization": "Bearer {0}".format(os.environ.get('translator'))
    }

    return requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                         json=body,
                         headers=headers)


def translate(target_lang: str, text: str):
    response = make_request(target_lang, text)
    if response.ok:
        content = json.loads(response.text)['translations'][0]
        print(f'Перевел с {content["detectedLanguageCode"]} на {target_lang}')
        print(content['text'])
    else:
        print(
            'Что-то пошло не так, проверьте параметры и подключение к интернету, текст для перевода заключите в кавычки')
        print('Код языка должен соответствовать формато ISO 639')
        print('https://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D0%B4%D1%8B_%D1%8F%D0%B7%D1%8B%D0%BA%D0%BE%D0%B2')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('lan', type=str, help='Язык на который перевести тексе')
    parser.add_argument('text', type=str, help='Текст для перевода')
    args = parser.parse_args()
    translate(args.lan, args.text)
