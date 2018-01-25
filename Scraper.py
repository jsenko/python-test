import asyncio

from bs4 import BeautifulSoup

from Download import Download


class Scraper:

    def __init__(self):
        self.__download = Download()

    @asyncio.coroutine
    def get_links(self, data):
        soup = BeautifulSoup(data, "html.parser")
        return list(filter(  # remove none
            lambda link: link,
            map(lambda tag: tag.get("href"), soup.find_all('a'))))

    @asyncio.coroutine
    def get_image_links(self, data):
        soup = BeautifulSoup(data, "html.parser")
        return list(filter(  # remove None
            lambda link: link,
            map(lambda tag: tag.get("src"), soup.find_all('img'))))
