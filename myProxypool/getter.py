from myProxypool.db import Redis
from myProxypool.crawler import *
import sys


class Getter():
    def __init__(self):
        self.__redis__ = Redis()
        self.__crawler__ = Crawler()

    def get(self):
        """
        获取代理，并存入数据库
        """
        if self.__redis__.count_available() <= 50:  # 可用代理小于50开始获取
            print("开始获取代理IP")
            for callback_label in range(self.__crawler__.__CrawlFuncCount__):
                callback = self.__crawler__.__CrawlFunc__[callback_label]
                sys.stdout.flush()
                for i in self.__crawler__.get_proxies(callback=callback):
                    self.__redis__.add(i)
