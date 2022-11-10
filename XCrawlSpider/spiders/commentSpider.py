import json

import execjs
import scrapy
import pandas as pd
from fake_useragent import UserAgent
import re

from XCrawlSpider.XCrawlSpider.items import XcrawlspiderItem


class CommentspiderSpider(scrapy.Spider):
    name = 'commentSpider'
    # allowed_domains = ['www.xxx.com']
    start_urls = [
        'https://www.dianping.com/shop/l2N3z4oFLOk7WGqB',
# 'https://www.dianping.com/shop/karMHeOL385peKUI',
# 'https://www.dianping.com/shop/k5Z182onb82QSoTC',
# 'https://www.dianping.com/shop/l5CHs4FzFlbjO3Mv',
# 'https://www.dianping.com/shop/H75mvLz9ndnTu0CO',
# 'https://www.dianping.com/shop/Ha7ZHpNpZSP3rWDP',
# 'https://www.dianping.com/shop/G9I488Usw4w3etHO',
# 'https://www.dianping.com/shop/H5SkrI00caDjLDLx',
# 'https://www.dianping.com/shop/G9gLh8Xzu6vF8YLh',
# 'https://www.dianping.com/shop/k8KMW3Auu4u5ejHG',
# 'https://www.dianping.com/shop/k3CbLChnx77zvDPY',
# 'https://www.dianping.com/shop/H9jC5kR5k62n4ORv',
# 'https://www.dianping.com/shop/EWa0dfaBc833Xlq9',
# 'https://www.dianping.com/shop/G1IGDTs5QBpnBvah',
# 'https://www.dianping.com/shop/G25nCMYY0mmTIqbO',
                # 'https://www.dianping.com/shop/H3hlnKQfgGAPlJG9',
                #   'https://www.dianping.com/shop/l2N3z4oFLOk7WGqB',
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
                'Cookie': '_lxsdk_cuid=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _lxsdk=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _hc.v=7db62757-4617-03c5-8227-a3b30a9803c6.1666510368; s_ViewType=10; WEBDFPID=5w0830xz08w35yvu197y7429u76xy6u781596x519x997958zvww6ww3-1981870520158-1666510519831MQUYSAUfd79fef3d01d5e9aadc18ccd4d0c95077639; ctu=3eada7613bfd5549da00debc4ee9ff6190908a18a5ec7383aee478c9ff16b664; cy=1946; cye=bange; dper=de89a983a903d8800d8406b5e096b455290424d5cd5b889f9d0313532957c54f62516b79d73044ac32008348c20522b285b6d3a3a37fcca240e3362fe3d1ded7; ll=7fd06e815b796be3df069dec7836c3df; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1667380665,1667492509,1667796220,1667797032; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1667797079; _lxsdk_s=1845066b67b-9cb-592-a2b%7C%7C88',
                'User-Agent': UserAgent().random,
                'Host': 'www.dianping.com',
                'Referer': 'https://www.dianping.com/shop/{}'.format(self.shop_id),
            }
            url = f'https://www.dianping.com/ajax/json/shopDynamic/allReview?shopId={self.shop_id}&cityId=8&shopType=10&tcv=4e7hqrxmfg&_token={self.get_token()}&uuid=7db62757-4617-03c5-8227-a3b30a9803c6.1666510368&platform=1&partner=150&optimusCode=10&originUrl=https://www.dianping.com/shop/l2g0kxUJRpV1bdZr'
            yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={'url': url, 'headers': headers})

    def parse(self, response):
        data = json.loads(response.text)
        # print(data.keys())
        # print(data)
        code = data['code']

        if code != 200:
            url = response.meta['url']
            headers = response.meta['headers']
            print(data)
            yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={'url': url, 'headers': headers})
        else:
            item = XcrawlspiderItem.items()
            mid_re = []

            reviewAllDOList = data['reviewAllDOList']
            for reviewDataVO in reviewAllDOList:
                # 评论体
                repl = reviewDataVO['reviewDataVO']['reviewData']['reviewBody']
                # print(repl)
                # print(repl)
                # repl = re.sub('<svgmtsi class="review">', '', reviewDataVO['reviewDataVO']['reviewData']['reviewBody'])
                # repl = re.sub('</svgmtsi>', '', repl)
                repl = re.sub(r'<br />', '', repl, re.DOTALL)
                repl = re.sub(r'<img class=".*?" src=".*?" alt=""/>', '', repl, re.DOTALL)
                repl = re.sub(r'&nbsp;', '', repl, re.DOTALL)
                mid_re.append(repl)
                print(repl)
            # print(reviewAllDOList)
            item['review'] = mid_re
            item['shop_name'] = self.shop_name
            with open('data.json', 'w', encoding='utf-8') as fp:
                json.dump(data, fp, ensure_ascii=False)

    def get_token(self):
        with open('./js/rohr.min.js', 'r', encoding='utf-8') as fp:
            js = fp.read()

        JS = execjs.compile(js)
        token = JS.call("hhh_token", f'https://www.dianping.com?shopId={self.shop_id}')
        return token
