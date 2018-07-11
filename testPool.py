import requests

PROXY_POOL_URL = 'http://localhost:5555/random'


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            proxy = response.text
            proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }
            return proxies
    except ConnectionError:
        return None

proxies = get_proxy()
print("代理IP为", proxies)
try:
    response = requests.get('http://www.baidu.com', proxies=proxies)
except:
    print("代理不可用")
else:
    if response.status_code==200:
        print("代理可用")
    else:
        print("代理不可用")

