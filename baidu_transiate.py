'''
    百度翻译数据抓取
'''
import execjs
import requests

class BaiduTranslateJS(object):
    '''
        百度翻译数据抓取
    '''
    def __init__(self, query):
        """
        :param query: 待翻译的内容
        cookie 值 可能会影响到翻译结果，可以将未登陆情况下百度翻译的cookie填写。
        """
        self.query = query
        self.url = "https://fanyi.baidu.com/v2transapi"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Cookie": "BAIDUID=AFB6E3FB47D3EEA8C525D02E728E0991:FG=1; BIDUPSID=AFB6E3FB47D3EEA8C525D02E728E0991; PSTM=1556177968; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; MCITY=-131%3A; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1556507678,1557287607,1557714510,1557972796; BDSFRCVID=xr-sJeCCxG3twro9YX2saOEfCZPT14fNd2s33J; H_BDCLCKID_SF=tR3fL-08abrqqbRGKITjhPrM2hKLbMT-027OKKO2b-oobfTyDRbHXULELn6TLT_J5eobot8bthF0HPonHj85j6bQ3J; PSINO=2; delPer=0; H_PS_PSSID=1450_28937_21095_18560_29064_28518_29098_28722_28963_28836_28584_26350; locale=zh; yjs_js_security_passport=5b9f340d92cf7400bd5ba82b49a65bc0520935cc_1558490261_js; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1558493551; to_lang_often=%5B%7B%22value%22%3A%22jp%22%2C%22text%22%3A%22%u65E5%u8BED%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22jp%22%2C%22text%22%3A%22%u65E5%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D"
        }
        self.data = {
            "from": "en",
            "to": "zh",
            "query": self.query,  # query 即我们要翻译的的内容
            "transtype": "translang",
            "simple_means_flag": "3",
            "sign": "",  # sign 是变化的需要我们执行js代码得到
            "token": "13508e550366f3004701d561721e12bd"  # token没有变化
        }

    def structure_form(self):
        """
        读取js文件
        执行js代码得到我们苦求的sign值
        构造新的表单
        :return:
        """
        with open('baidu.js', 'r', encoding='utf-8') as f:
            ctx = execjs.compile(f.read())
        sign = ctx.call('e', self.query)  # e为js代码里的函数名  # self.query为要查的单词,也就是e函数需要填写的参数  sign为js代码执行的返回的结果
        # print(sign)
        # sign成功获取，写入date
        self.data['sign'] = sign

    def get_response(self):
        """
        通过构造的新的表单数据，访问api，获取翻译内容
        :return: 翻译结果
        """
        self.structure_form()
        response = requests.post(self.url, headers=self.headers, data=self.data).json()
        # print(response)
        r = response['trans_result']['data'][0]['dst']
        return r


if __name__ == '__main__':
    while True:
        word = input('请输入要查的单词:')
        baidu_translate_spider = BaiduTranslateJS(word)
        result = baidu_translate_spider.get_response()
        print(result)