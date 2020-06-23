import re
import os.path
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Parser:
    host = 'https://stopgame.ru'
    url = 'https://stopgame.ru/review/new'

    lastkey = ''
    lastkey_file = ''

    def __init__(self, lastkey_file):
        
        self.lastkey_file = lastkey_file

        if os.path.exists(lastkey_file):
            self.lastkey = open(lastkey_file, 'r').read()
        else:
            with(open(lastkey_file, 'w')) as file:
                self.lastkey = self.get_lastkey()
                file.write(self.lastkey)

    def new_games(self):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.content, 'lxml')

        new = []
        items = soup.select('.tiles > .items > .item > a')

        for item in items:
            key = self.parse_href(item['href'])
            if self.lastkey < key:
                new.append(item['href'])

        return new

    def game_info(self, uri):
        link = self.host + uri
        res = requests.get(link)
        soup = BeautifulSoup(res.content, 'lxml')

        poster = re.match(r'background-image:\s*url\((.+?)\)', soup.select('.image-game-logo > .image')[0]['style'])

		# remove some stuff
        remels = soup.select('.article.article-show > *')
        for remel in remels:
            remel.extract()

		# form data
        info = {
            "id": self.parse_href(uri),
            "title": soup.select('.article-title > a')[0].text,
            "link": link,
            "image": poster.group(1),
            "score": self.identify_score(soup.select('.game-stopgame-score > .score')[0]['class'][1]),
            "excerpt": soup.select('.article.article-show')[0].text[0:200] + '...'
        }

        return info

    def download_image(self, url):
        res = requests.get(url, allow_redirects=True)

        a = urlparse(url)
        filename = f'img/{os.path.basename(a.path)}'
        open(filename, 'wb').write(res.content)

        return filename

    def identify_score(self, score):
        if score == 'score-1':
            return "Мусор 👎"
        elif score == 'score-2':
            return "Проходняк ✋"
        elif score == 'score-3':
            return "Похвально 👍"
        elif score == 'score-4':
            return "Изумительно 👌"

    def get_lastkey(self):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.content, 'lxml')

        items = soup.select('.tiles > .items > .item > a')
        print(items)
        # return self.parse_href(items[0]['href'])

    def parse_href(self, href):
        result = re.match(r'\/show\/(\d+)', href)
        return result.group(1)

    def update_lastkey(self, new_key):
        self.lastkey = new_key

        with open(self.lastkey_file, 'r+') as file:
            data = file.read()
            file.seek(0)
            file.write(str(new_key))
            file.truncate()

        return new_key
