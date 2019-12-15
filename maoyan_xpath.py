'''
    利用xpath表达式抓取猫眼电影top100
'''

from lxml import etree
import requests
import time
import random
import csv


class MaoYanSpider(object):
    def __init__(self):
        self.url = 'https://maoyan.com/board/4?offset={}'
        self.ua_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
        ]

    # 获取响应
    def get_page(self, url):
        # 每次使用随机的User-Agent
        self.headers = {'User-Agent': random.choice(self.ua_list)}
        html = requests.get(url=url, headers=self.headers).content.decode()
        # 　调用解析函数,提取数据
        self.get_data(html)

    # 提取数据
    def get_data(self, html):
        # 创建解析对象
        parse_html = etree.HTML(html)
        # 1.基准xpath:匹配每个电影信息的节点对象
        r_list = parse_html.xpath('//dl[@class="board-wrapper"]/dd')
        move_dict = {}
        # 2.for依次遍历每个节点对象,获取信息
        for dd in r_list:
            move_dict['name'] = dd.xpath('./a/@title')[0].strip()
            move_dict['actor'] = dd.xpath('.//p[@class="star"]/text()')[0].strip()
            move_dict['s_time'] = dd.xpath('.//p[@class="releasetime"]/text()')[0].strip()
            print(move_dict)
        # self.write_page(r_list)

    # 保存数据,保存到csv  writerows
    def write_page(self, r_list):
        filename = '猫眼电影top100.csv'
        # 空列表,最终writerows参数:[(),(),()]
        file_list = []
        fd = open(filename, 'a+', encoding='utf-8')
        writer = csv.writer(fd)
        for item in r_list:
            # 把处理过的数据定义成元组
            t = (item[0], item[1].strip(), item[2].strip()[5:15])
            file_list.append(t)
        writer.writerows(file_list)
        fd.close()

    # 主函数
    def main(self):
        for page in range(1, 11):
            offset = (page - 1) * 10
            url = self.url.format(offset)
            self.get_page(url)
            time.sleep(random.randint(1, 3))

        print('抓取成功')


if __name__ == "__main__":
    start = time.time()
    spider = MaoYanSpider()
    spider.main()
    end = time.time()
    print('花费时间:%.2f' % (end - start))
