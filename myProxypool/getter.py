from myProxypool.db import Redis
from myProxypool.crawler import *
import sys


class Getter():
    def __init__(self):
        self.__redis = Redis()
        self.__crawler = Crawler()

    def get(self):
        """
        获取代理，并存入数据库
        """
        if self.__redis.count_available() <= 50:  # 可用代理小于50开始获取
            print("开始获取代理IP")
            for callback_label in range(self.__crawler.__CrawlFuncCount__):
                callback = self.__crawler.__CrawlFunc__[callback_label]
                sys.stdout.flush()
                for i in self.__crawler.get_proxies(callback=callback):
                    self.__redis.add(i)
