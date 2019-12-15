import requests
import time
import random
from hashlib import md5


# 获取salt sign ts
def get_salt_sign_ts(word):
    # ts
    ts = str(int(time.time() * 1000))
    # salt
    salt = ts + str(random.randint(0, 9))
    # sign
    string = 'fanyideskweb' + word + salt + "n%A-rKaT5fb[Gy?;N5@Tj"
    s = md5()
    s.update(string.encode())
    sign = s.hexdigest()
    return salt, ts, sign


# 破解有道翻译
def attack_yd(word):
    salt, ts, sign = get_salt_sign_ts(word)
    # url地址为F12-->headers-->general-->request url
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    proxies = {
        'http': 'http://118.173.233.37:45592',
        'https': 'https://118.173.233.37:45592'
    }
    # headers
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "238",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "OUTFOX_SEARCH_USER_ID=-1449945727@10.169.0.82; OUTFOX_SEARCH_USER_ID_NCOO=1492587933.976261; JSESSIONID=aaa5_Lj5jzfQZ_IPPuaSw; ___rl__test__cookies=1559193524685",
        "Host": "fanyi.youdao.com",
        "Origin": "http://fanyi.youdao.com",
        "Referer": "http://fanyi.youdao.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    # data:FormData为字典
    data = {
        'i': word,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'ts': ts,
        'bv': 'cf156b581152bd0b259b90070b1120e6',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }

    html_json = requests.post(url=url, data=data, headers=headers, proxies=proxies).json()
    res = html_json['translateResult'][0][0]['tgt']
    return res


if __name__ == '__main__':
    word = input('请输入要翻译的单词:')
    result = attack_yd(word)
    print(result)
