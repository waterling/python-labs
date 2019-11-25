"""
Вход: файл guess.txt содержащий имена для угадывания

(например из http://www.biographyonline.net/people/famous-100.html можно взять имена)


Написать игру "Угадай по фото"

3 уровня сложности:
1) используются имена только 1-10
2) имена 1-50
3) имена 1-100

- из используемых имен случайно выбрать одно
- запустить поиск картинок в Google по выбранному
- получить ~30-50 первых ссылок на найденные по имени изображения
- выбрать случайно картинку и показать ее пользователю для угадывания
  (можно выбрать из выпадающего списка вариантов имен)
- после выбора сказать Правильно или Нет

п.с. сделать серверную часть, т.е. клиент играет в обычном браузере обращаясь к веб-серверу.

п.с. для поиска картинок желательно эмулировать обычный пользовательский запрос к Google
или можно использовать и Google image search API
https://ajax.googleapis.com/ajax/services/search/images? или др. варианты
НО в случае API нужно предусмотреть существующие ограничения по кол-ву запросов
т.е. кешировать информацию на случай исчерпания кол-ва разрешенных (бесплатных)
запросов или другим образом обходить ограничение. Т.е. игра не должна прерываться после N запросов (ограничение API)


п.с. желательно "сбалансировать" параметры поиска (например искать только лица,
использовать только первые 1-30 найденных и т.п.)
для минимизации того что найденная картинка не соответствует имени

"""

"AIzaSyDGhEBBg-PmsT2wgtUPr0jM8LQRWQ6HEBw"

import urllib.request
from urllib.request import Request, urlopen
from lxml import html
import sys

""""
def init_names():
    req = Request(
        "https://www.biographyonline.net/people/famous-100.html",
        headers={'User-Agent': 'Mozilla/5.0'})
    html_content = urlopen(req).read()

    tree = html.fromstring(html_content)

    name = []
    for i in range(1, 100):
        name.append(tree.xpath('(.//*[@class=\'post-content clearfix\']/ol/li)[' + str(i) + ']/a/text()'))
    return name
"""


def read_names(filename):
    f = open(filename, "r")

    fl = f.readlines()

    names = []
    for name in fl:
        names.append(name)

    return names


from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class HTTPServerQuiz(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        smth = sys.argv[1]

        names = read_names(sys.argv[1])

        import random
        index = random.randint(0, 99)

        print(index)

        name = names[index]
        name_without_eol = name[:name.find('\n')]
        photo = self.get_photo(name_without_eol)[0]

        print(name_without_eol + ' - ' + photo)

        response = {
            'photo': photo,
            'answer': name_without_eol
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(response), encoding='utf-8'))

    def get_photo(self, name):
        url = "https://www.google.ru/search?site=&tbm=isch&source=hp&biw=1600&bih=1600&q=" + name.replace(" ", "%20")

        req = Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0'})
        html_content = urlopen(req).read()

        tree = html.fromstring(html_content)

        import random
        ph = tree.xpath('(.//*[@target="_blank"]/img)[' + str(random.randint(1, 10)) + ']/@src')
        return ph


def name_foto_quiz():
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, HTTPServerQuiz)

    httpd.serve_forever()


if __name__ == '__main__':
    name_foto_quiz()
