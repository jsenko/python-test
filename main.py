import asyncio
import atexit

from Spider import Spider

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    root_spider = Spider(loop, "https://exponea.com")
    loop.run_until_complete(root_spider.run())
    atexit.register(loop.close)
