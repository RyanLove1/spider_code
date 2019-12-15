'''
    抓取豆瓣电影动态加载的数据
'''

import requests


class DoubanSpider(object):
    def __init__(self):
        self.url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start=0&limit={}'
        self.headers = {
            'Accept': '*/*',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'll="108288"; bid=Y2zsxhJpCLY; __utmc=30149280; __utmc=223695111; __yadk_uid=g1xlgXasHxITvN8epzBRD76f3UUp6Eta; trc_cookie_storage=taboola%2520global%253Auser-id%3D06d16168-2035-4efd-8827-7fe99a9279c6-tuct3df8bc5; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1563871699%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DEswlNmfqk8tgwswOF35Q34qWr3a8CGRyCxHVqFl6A9U4JWODZKj1pQuAdkFHSCeR%26wd%3D%26eqid%3Df839835a0013d672000000035d36c922%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.1434879993.1563787284.1563787284.1563871699.2; __utmb=30149280.0.10.1563871699; __utmz=30149280.1563871699.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=223695111.42559862.1563787284.1563787284.1563871699.2; __utmb=223695111.0.10.1563871699; __utmz=223695111.1563871699.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _vwo_uuid_v2=D1E8D3E3F2EA09BE84710368F2E8116C0|9229ac5ac0bc70539922f568a8116fc4; _pk_id.100001.4cf6=d1ed95e44103ad17.1563787284.2.1563872775.1563787284.',
            'Host': 'movie.douban.com',
            'Referer': 'https://movie.douban.com/typerank?type_name=%E5%89%A7%E6%83%85&type=11&interval_id=100:90&action=',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

    # 请求+解析
    def get_film_info(self, url):
        # res.json --> 返回python数据类型(列表或字典)
        # html_json:[{},{},{}]
        html_json = requests.get(url=url, headers=self.headers).json()
        # for变量每个电影信息
        for film in html_json:
            # 名称
            name = film['title']
            # 评分
            score = film['score']
            print(name, score)

    # 主函数
    def main(self):
        limit = input('请输入要抓取的电影数量:')
        url = self.url.format(limit)
        self.get_film_info(url)


if __name__ == "__main__":
    spider = DoubanSpider()
    spider.main()
