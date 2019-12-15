import requests
from urllib import parse
from lxml import etree


class BaiduImgSpider(object):
    def __init__(self):
        self.url = 'http://tieba.baidu.com/f?{}'
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}

    # 获取帖子链接
    def get_tlink(self, url):
        html = requests.get(url, headers=self.headers).text
        # 提取帖子链接
        parse_html = etree.HTML(html)
        tlink_list = parse_html.xpath(
            '//*[@id="thread_list"]/li//div[@class="t_con cleafix"]/div/div/div/a/@href')
        # tlink_list: ['/p/23234','/p/9032323']
        for tlink in tlink_list:
            t_url = 'http://tieba.baidu.com' + tlink
            # 提取图片链接并保存
            self.get_imglink(t_url)

    # 获取图片链接
    def get_imglink(self, t_url):
        res = requests.get(t_url, headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        # 提取图片链接
        parse_html = etree.HTML(html)
        # 匹配图片和视频的xpath表达式,中间加或 |
        imglink_list = parse_html.xpath(
            '//div[@class="d_post_content_main  d_post_content_firstfloor"]//div[@class="d_post_content j_d_post_content "]/img/@src | //div[@class="video_src_wrapper"]/embed/@data-video')

        for imglink in imglink_list:
            self.write_img(imglink)

    # 保存图片
    def write_img(self, imglink):
        res = requests.get(imglink, headers=self.headers)
        # 切取链接的后10位作为文件名
        filename = imglink[-10:]
        with open(filename, 'wb') as f:
            f.write(res.content)
            print('%s下载成功' % filename)

    # 指定贴吧名称,起始页和终止页,爬取图片
    def main(self):
        name = input('请输入贴吧名:')
        begin = int(input('请输入起始页:'))
        end = int(input('请输入终止页:'))
        for page in range(begin, end + 1):
            # 查询参数编码
            params = {
                'kw': name,
                'pn': str((page - 1) * 50)
            }
            params = parse.urlencode(params)
            url = self.url.format(params)
            # 开始获取图片
            self.get_tlink(url)


if __name__ == '__main__':
    spider = BaiduImgSpider()
    spider.main()
