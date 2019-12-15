'''
    抓取民政部数据(行政区划代码)
'''

import requests
from lxml import etree
import pymysql
import re


class GovementSpider(object):
    def __init__(self):
        self.one_url = 'http://www.mca.gov.cn/article/sj/xzqh/2019/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
        }
        self.db = pymysql.connect('localhost', 'root', '123456', 'govdb', charset='utf8')
        self.cursor = self.db.cursor()

    # 提取二级页面链接(假链接)
    def get_false_link(self):
        html = requests.get(url=self.one_url, headers=self.headers).content.decode('utf-8', 'ignore')
        parse_html = etree.HTML(html)
        # xpath://a[@class='artitlelist']
        r_list = parse_html.xpath("//a[@class='artitlelist']")
        for r in r_list:
            # 或者这么找title属性值
            # title = r.get('title')
            title = r.xpath("./@title")[0]
            # 利用正则找到第一个自己需要的title里面的地址(第一个一般都是最新的)
            if re.findall(r'.*?中华人民共和国县以上行政区划代码.*?', title, re.S):
                # 获取到第1个就停止即可，第1个永远是最新的链接
                two_link = 'http://www.mca.gov.cn' + r.xpath('./@href')[0]
                return two_link

    # 提取真是的二级页面链接(返回数据的链接)
    def get_true_link(self):
        two_false_link = self.get_false_link()
        html = requests.get(url=two_false_link, headers=self.headers).text
        pattern = re.compile(r'window.location.href="(.*?)"', re.S)
        real_link = pattern.findall(html)[0]

        # 实现增量爬取
        # 到version表中查询是否有real_link
        # 有:数据最新  没有:抓数据
        self.cursor.execute('select * from version where link="{}"'.format(real_link))
        # 不为空元组,链接已存在(不需要抓取数据)
        if self.cursor.fetchall():
            print('数据已是最新')
        else:
            # 先抓取数据
            self.get_data(real_link)
            # 把real_link链接插入到version表中
            ins = "insert into version values(%s)"
            self.cursor.execute(ins, [real_link])
            self.db.commit()

    # 真正提取数据函数
    def get_data(self, real_link):
        html = requests.get(url=real_link, headers=self.headers).text
        # 基本xpath: //tr[@height="19"]
        parse_html = etree.HTML(html)
        tr_list = parse_html.xpath('//tr[@height="19"]')
        for tr in tr_list:
            # code: ./td[2]/text()
            code = tr.xpath('./td[2]/text()')[0]
            # name: ./td[3]/text()
            name = tr.xpath('./td[3]/text()')[0]
            print(name, code)

    # 主函数
    def main(self):
        self.get_true_link()


if __name__ == "__main__":
    spider = GovementSpider()
    spider.main()
