'''
    抓取代理ip
'''

import requests
from lxml import etree
from fake_useragent import UserAgent

url = 'https://www.kuaidaili.com/free/inha/{}/'


# 获取User-Agent
def get_random_ua():
    ua = UserAgent()
    return ua.random


headers = {'User-Agent': get_random_ua()}


# 获取所有代理ip地址和端口号
def get_ip_list(url):
    # 获取
    html = requests.get(url, headers=headers, verify=False).text
    # 解析
    parse_html = etree.HTML(html)
    r_list = parse_html.xpath('//tr')
    proxies_list = []  # 存放所有ip和port端口
    for r in r_list[1:]:
        IP = r.xpath('./td[@data-title="IP"]/text()')[0]
        PORT = r.xpath('./td[@data-title="PORT"]/text()')[0]
        proxies_list.append(
            {
                'http': 'http://{}:{}'.format(IP, PORT),
                'https': 'https://{}:{}'.format(IP, PORT)
            }
        )
    # print(proxies_list)
    return proxies_list


# 测试代理,建立代理IP池
def proxy_pool():
    # 调用上面函数
    for i in range(1, 5):
        url2 = url.format(i)
        proxy_list = get_ip_list(url2)
        for proxy in range(len(proxy_list) - 1, -1, -1):
            try:
                res = requests.get(url='http://httpbin.org/get', headers=headers, proxies=proxy_list[proxy], timeout=6)
                with open("proxies_ip.txt", "a") as f:
                    f.write(proxy_list[proxy])
            except Exception as e:
                print(proxy_list[proxy])
                print('不能用')
                proxy_list.remove(proxy_list[proxy])

        print(proxy_list)


if __name__ == "__main__":
    proxy_pool()
