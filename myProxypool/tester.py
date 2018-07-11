import asyncio
import aiohttp
import sys
from myProxypool.db import Redis
from myProxypool.setting import VALID_STATUS_CODES, BATCH_TEST_SIZE


class Tester():
    def __init__(self):
        self.semaphore = asyncio.Semaphore(500)
        self.redis = Redis()

    async def aioget(self, url, proxy):
        proxies = 'http://' + proxy
        try:
            async with self.semaphore:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, proxy=proxies, timeout=5) as response:
                        if response.status in VALID_STATUS_CODES:
                            print(proxy, "可用")
                            self.redis.available(proxy)
        except Exception:
            print(proxy, "不可用")
            self.redis.decrease(proxy)

    def test(self):
        print("开始测试代理IP")
        if self.redis.count_all() > 0:
            tasks = [asyncio.ensure_future(self.aioget('https://www.baidu.com/', i.decode())) for i in
                     self.redis.get()]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
            sys.stdout.flush()
