'''
    抓取哔哩哔哩小视频
'''

import requests


class BilibiliSpider(object):
    def __init__(self):
        self.url = 'http://api.vc.bilibili.com/board/v1/ranking/top?page_size=10&next_offset={}&tag=%E4%BB%8A%E6%97%A5%E7%83%AD%E9%97%A8&platfo'
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'http://vc.bilibili.com',
            'Referer': 'http://vc.bilibili.com/p/eden/rank',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        }

    # 请求 + 解析
    def get_film(self, url):
        html_json = requests.get(url, headers=self.headers).json()

        film_link_list = html_json['data']['items']
        for film_link in film_link_list:
            down_link = film_link['item']['video_playurl']
            html = requests.get(down_link, headers=self.headers).content
            filename = down_link[-10:] + '.mp4'
            with open(filename, 'wb') as f:
                f.write(html)

    # 主函数
    def main(self):
        for i in range(1, 3):
            page = i * 10 + 1
            url = self.url.format(page)
            self.get_film(url)
            print('第{}页视频下载完成!'.format(i))

if __name__ == "__main__":
    spider = BilibiliSpider()
    spider.main()
