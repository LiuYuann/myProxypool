from redis import StrictRedis
from random import choice
from myProxypool.setting import *


class Redis():
    def __init__(self):
        self.__redis__ = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)

    def add(self, proxy):
        if self.count_all() >= POOL_UPPER_THRESHOLD:
            pass
        else:
            self.__redis__.zadd('proxy', 100, proxy)

    def decrease(self, proxy):
        if self.__redis__.zscore('proxy', proxy) < 80:
            self.__redis__.zrem('proxy', proxy)
        else:
            self.__redis__.zincrby('proxy', proxy, -5)
    def count_available(self):
        """
        :return: 当前可用代理总数
        """
        return self.__redis__.zcount('proxy', 100, 100)

    def count_all(self):
        """
        :return: 当前代理总数
        """
        return self.__redis__.zcount('proxy', 0, 100)

    def get(self):
        return self.__redis__.zrevrange('proxy', 0, BATCH_TEST_SIZE - 1)#取出分数前BATCH_TEST_SIZE名的记录用来测试

    def available(self, proxy):
        self.__redis__.zadd('proxy', 100, proxy)

    def random(self):
        result = self.__redis__.zrevrange('proxy', 0, 9, False)#取出分数前十名的记录
        if len(result):
            return choice(result).decode()
        else:
            return None
