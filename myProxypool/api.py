from flask import Flask, g

from myProxypool.db import Redis

__all__ = ['app']

app = Flask(__name__)


@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/random')
def get_proxy():
    """
    Get a proxy
    :return: 随机代理
    """
    redis = Redis()
    return redis.random()


@app.route('/count')
def get_counts():
    """
    Get the count of proxies
    :return: 可用代理总量
    """
    redis = Redis()
    return "当前可用代理"+str(redis.count_available())+"个"


if __name__ == '__main__':
    app.run()
