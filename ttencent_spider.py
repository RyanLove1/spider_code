'''
    腾讯招聘信息抓取
'''

import requests


class TtencentSpider(object):
    def __init__(self):
        self.url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1563879436992&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cookie': '_ga=GA1.2.1063279804.1563274546; pgv_pvi=5160086528; _gcl_au=1.1.821423378.1563274547; loading=agree',
            'referer': 'https://careers.tencent.com/search.html?index=1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
        }

    # 请求+解析
    def get_info(self, url):
        html_json = requests.get(url, headers=self.headers).json()
        msg_all = html_json['Data']['Posts']
        for msg in msg_all:
            RecruitPostName = msg['RecruitPostName']
            LocationName = msg['LocationName']
            Responsibility = msg['Responsibility']
            print(RecruitPostName)
            print(LocationName)
            print(Responsibility)

    # 主函数
    def main(self):
        for page in range(1, 5):
            url = self.url.format(page)
            self.get_info(url)


if __name__ == '__main__':
    spider = TtencentSpider()
    spider.main()
