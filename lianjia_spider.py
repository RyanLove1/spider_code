from lxml import etree
import time
import requests
import random


class LianJiaSpider(object):
    def __init__(self):
        self.url = 'https://bj.lianjia.com/ershoufang/pg{}/'
        self.ua_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
        ]

    def get_page(self, url):
        self.headers = {'User-Agent': random.choice(self.ua_list)}
        res = requests.get(url, headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        self.parse_page(html)

    def parse_page(self, html):
        parse_html = etree.HTML(html)
        r_list = parse_html.xpath('//ul[@class="sellListContent"]/li[@class="clear LOGCLICKDATA"] | //ul[@class="sellListContent"]/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]')
        for dd in r_list:
            address = dd.xpath('.//a[@data-el="region"]/text()')[0].strip()
            totle_price = dd.xpath('.//div[@class="totalPrice"]/span/text()')[0].strip() + '万'
            unit_price = dd.xpath('.//div[@class="unitPrice"]/span/text()')[0].strip()[2:]
            print(address,totle_price,unit_price)



    def main(self):
        for page in range(3, 4):
            url = self.url.format(page)
            self.get_page(url)
        print('抓取完成')

if __name__ == '__main__':
    start = time.time()
    spider = LianJiaSpider()
    spider.main()
    end = time.time()
    print('执行时间:%.2f' % (end - start))
