import asyncio

import re

from Download import Download
from Scraper import Scraper


class Spider:
    RE_EXPONEA = re.compile("^https?://[^/]*exponea.com(/.*)?$")
    downloaded = []
    visited = []

    def __init__(self, loop, url):
        self.__url = self.__remove_trailing_slash(url)
        self.__loop = loop
        self.__downloader = Download()
        self.__scraper = Scraper()

    def __gen_file_name(self, link):
        return link.replace("/", "_")

    def __remove_trailing_slash(self, url):
        if url[-1] == "/":
            return url[:-1]
        else:
            return url

    def __is_exponea(self, url):
        return Spider.RE_EXPONEA.match(url)

    # if i used selenium this would be easier (following links),
    # but i wanted to keep it simple, so here we go:
    # (i'd use selenium or some scraping framework next time)
    @asyncio.coroutine
    def _sanitize_url(self, url, filter_exponea=False):
        if len(url) > 500:
            print("Somethings probably wrong (loop?): " + url)  # or base64
            return None

        if url.startswith("http") and (not filter_exponea or self.__is_exponea(url)):  # refactor this bit to be generic
            return url

        if url.startswith("//") and (not filter_exponea or self.__is_exponea("http:" + url)):
            return "http:" + url

        if url.startswith("/"):
            return self.__url + url

        # todo there are some base64 encoded images rejected

        print("Sanitize: Rejected " + url)
        return None

    @asyncio.coroutine
    def run(self):
        print("Processing " + self.__url)
        Spider.visited.append(self.__url)
        # get images

        page = yield from self.__downloader.download_data_url(self.__url)
        if not page:
            return
        imglinks = yield from self.__scraper.get_image_links(page)
        for link in imglinks:
            sanitized = yield from self._sanitize_url(link)
            if sanitized and (sanitized not in Spider.downloaded):
                Spider.downloaded.append(sanitized)
                yield from self.__downloader.download_image_url(sanitized, self.__gen_file_name(sanitized))

        # SPAWN!
        links = yield from self.__scraper.get_links(page)
        for link in links:
            sanitized = yield from self._sanitize_url(link, filter_exponea=True)
            if sanitized and (sanitized not in Spider.visited):
                next = Spider(self.__loop, sanitized)
                yield from next.run()
