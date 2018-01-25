import asyncio
import aiohttp


class Download:
    __session = None

    def __init__(self):
        pass

    @asyncio.coroutine
    def __init(self):
        if not Download.__session:
            Download.__session = aiohttp.ClientSession()

    def __process_base64(self, url):
        # data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZlcnNpb249IjEuMCIgd2lkdGg9IjE0NDAiIGhlaWdodD0iNDUwIiA+PC9zdmc+
        # todo
        pass

    @asyncio.coroutine
    def download_image_url(self, url, name):
        data = yield from self.download_data_url(url, contains_mime_type="image")
        if not data:
            return None
        print("Downloaded: " + url)
        with open(name, "w+b") as f:
            f.write(data)
        pass

    @asyncio.coroutine
    def download_data_url(self, url, contains_mime_type=""):
        yield from self.__init()
        try:
            resp = (yield from Download.__session.head(url))  # check first
        except aiohttp.client_exceptions.InvalidURL as e:
            return None  # todo check directly
        if resp.status >= 400:
            print("Failed " + str(resp.status) + " " + url)
            return None

        content_type = list(filter(lambda hk: hk.lower() == "content-type", resp.headers.keys()))

        if content_type and (contains_mime_type in resp.headers[content_type[0]]):
            resp = (yield from Download.__session.get(url))
            data = yield from resp.read()
            return data
        return None

