import json

import execjs
import scrapy
import pandas as pd
from fake_useragent import UserAgent


class CommentspiderSpider(scrapy.Spider):
    name = 'commentSpider'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.dianping.com/shop/H3hlnKQfgGAPlJG9',
                  # 'https://www.dianping.com/shop/l2N3z4oFLOk7WGqB',
                  # 'https://www.dianping.com/shop/H37lWh9emnhXz7LY'
                  ]

    # def __init__(self):
    #     path = r'./csv/丁青县.csv'
    #     pds = pd.read_csv(path)
    #     self.start_urls = pds['url'].values
    #     # print(self.start_urls)
    def start_requests(self):
        for url in self.start_urls:
            self.shop_id = url.split('/')[-1]
            headers = {
                'Cookie': 'fspop=test; cy=153; cye=rizhao; _lxsdk_cuid=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _lxsdk=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _hc.v=7db62757-4617-03c5-8227-a3b30a9803c6.1666510368; s_ViewType=10; WEBDFPID=5w0830xz08w35yvu197y7429u76xy6u781596x519x997958zvww6ww3-1981870520158-1666510519831MQUYSAUfd79fef3d01d5e9aadc18ccd4d0c95077639; dper=ab7eef6129a412b25b0ac3854ff9e3bd0bf35371e8df4c10679b2f4ae332c4520bd2d188510101887353e78941e52b4a8a57ffa532d2ed4c662b55acd1dda1b993627620ed1e01619351ee224709f7c84571b76e4d9481e5692247f0803176e1; ua=dpuser_3830243167; ctu=3eada7613bfd5549da00debc4ee9ff6190908a18a5ec7383aee478c9ff16b664; _lx_utm=utm_source=bing&utm_medium=organic; ll=7fd06e815b796be3df069dec7836c3df; dplet=a1ded827ad67a2f1eaf855c2d2249de0; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666950926,1666995148,1667001764,1667098148; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1667099170; _lxsdk_s=18426cafb66-ae0-e72-2ab||121',
                'User-Agent': UserAgent().random,
                'Host': 'www.dianping.com',
                'Referer': 'https://www.dianping.com/shop/{}'.format(self.shop_id),
            }
            url = 'https://www.dianping.com/ajax/json/shopDynamic/allReview?shopId={}&cityId=8&shopType=10&tcv=4e7hqrxmfg&_token={}&uuid=7db62757-4617-03c5-8227-a3b30a9803c6.1666510368&platform=1&partner=150&optimusCode=10&originUrl=https://www.dianping.com/shop/l2g0kxUJRpV1bdZr'.format(
                self.shop_id, self.get_token())
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        print(data.keys())
        # print(response.url)
        # print(response.headers)
        # rs = json.loads(response.text)
        # item = response.meta['item']
        # data = item
        # print(response)
        # print("paser")

    def get_token(self):
        with open('./js/rohr.min.js', 'r', encoding='utf-8') as fp:
            js = fp.read()

        JS = execjs.compile(js)
        token = JS.call("hhh_token", 'https://www.dianping.com?shopId={}'.format(self.shop_id))
        return token
