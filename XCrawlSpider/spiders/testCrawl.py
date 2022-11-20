import scrapy
import json
import random
import time

import execjs
import scrapy
import pandas as pd
from fake_useragent import UserAgent
import re

class TestcrawlSpider(scrapy.Spider):
    name = 'testCrawl'
    # allowed_domains = ['xxx.com']
    # start_urls = ['http://xxx.com/']

    def start_requests(self):
        # 读取json
        with open('./json/city_list.json', 'r', encoding='utf-8') as fp:
            data = json.load(fp)

        with open('XCrawlSpider/spiders/json/review.json', 'r', encoding='utf-8') as fp:
            self.review = json.load(fp)

        city_list = data.keys()
        # print(city_list)
        # city_list = ['三亚']
        # 读取csv
        path = r'./log.csv'
        log = pd.read_csv(path).iloc[:, 1].values
        # print(city_list)
        for city in city_list:
            if city not in log:
                # path.append(f'./csv/{city}.csv')
                pds = pd.read_csv(f'./csv/{city}.csv')
                # for urls in ['https://www.dianping.com/shop/G9X32n6EvRA5uwdp']:
                for urls in pds.iloc[:, 1].values:
                    self.shop_id = urls.split('/')[-1]
                    # print(self.shop_id)
                    cookie = [
                        's_ViewType=10; _lxsdk_cuid=18431b3e864c8-01933c488e725a-26021b51-384000-18431b3e864c8; _lxsdk=18431b3e864c8-01933c488e725a-26021b51-384000-18431b3e864c8; _hc.v=652bc9d6-1f70-3c7b-55b7-445886fd6498.1667281185; WEBDFPID=9y5708w5vu5059xv0u815u3519wx6y2881568y530zu979588v74z2vx-1982641217806-1667281217370SOQMUYYfd79fef3d01d5e9aadc18ccd4d0c95071750; ctu=3eada7613bfd5549da00debc4ee9ff61cf0c6fe7b9b663833fc2c67b06018752; fspop=test; cy=57; cye=alashan; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1668092759,1668093555,1668784143,1668914212; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1668914218; _lxsdk_s=1849309ec6d-287-bb3-f6%7C%7C46',
                        '_lxsdk_cuid=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _lxsdk=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _hc.v=9fec2d1c-9253-9f08-843d-4d8d0bd47aaa.1668095623; s_ViewType=10; fspop=test; cy=57; cye=alashan; __utma=205923334.1124010926.1668848108.1668848108.1668848108.1; __utmz=205923334.1668848108.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); WEBDFPID=8x7y7yz136w6589yz97u5zwy8z6x294v8151u8y12zx979588w9915xu-1984208257365-1668848257101QMIMWGKfd79fef3d01d5e9aadc18ccd4d0c95071406; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1668781057,1668781856,1668846571,1668911845; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1668911852; _lxsdk_s=18492e5cd1c-082-228-b66%7C%7C54',
                    ]
                    headers = {
                        # 'Cookie': '_lxsdk_cuid=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _lxsdk=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _hc.v=7db62757-4617-03c5-8227-a3b30a9803c6.1666510368; s_ViewType=10; WEBDFPID=5w0830xz08w35yvu197y7429u76xy6u781596x519x997958zvww6ww3-1981870520158-1666510519831MQUYSAUfd79fef3d01d5e9aadc18ccd4d0c95077639; ctu=3eada7613bfd5549da00debc4ee9ff6190908a18a5ec7383aee478c9ff16b664; cy=1946; cye=bange; dper=de89a983a903d8800d8406b5e096b455290424d5cd5b889f9d0313532957c54f62516b79d73044ac32008348c20522b285b6d3a3a37fcca240e3362fe3d1ded7; ll=7fd06e815b796be3df069dec7836c3df; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1667380665,1667492509,1667796220,1667797032; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1667797079; _lxsdk_s=1845066b67b-9cb-592-a2b%7C%7C88',
                        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                        'User-Agent': UserAgent().random,
                        'Host': 'www.dianping.com',
                        'Referer': 'https://www.dianping.com/shop/{}'.format(self.shop_id),
                        'Cookie': random.choice(cookie)
                    }
                    # 获取十位时间戳
                    timestamp = int(time.time())
                    uuid = f'{random.randint(1, 9)}fec2d1c-9253-9f08-843d-4d8d0bd47aaa.{timestamp}'
                    url = f'https://www.dianping.com/ajax/json/shopDynamic/allReview?shopId={self.shop_id}&cityId=2372&shopType=10&tcv=jo0yrd5tgg&_token={self.get_token()}&uuid={uuid}&platform=1&partner=150&optimusCode=10&originUrl=https://www.dianping.com/shop/{self.shop_id}'
                    print(f"*******step 1:********\nshop_id:\t{self.shop_id}\nurl:\t{url}")
                    shop_url = urls
                    time.sleep(random.randint(1, 3))
                    yield scrapy.Request(url=url, headers=headers, callback=self.parse_info,
                                         meta={'url': url, 'headers': headers, 'city': city, 'shop_url': shop_url},
                                         dont_filter=True)
                    # yield scrapy.http.Request(url=url, headers=headers, callback=self.parse, meta={'url': url, 'headers': headers})

    """
        获取加密的评论数据
        callback: parse_info
        meta: 加密后的评论，城市名称，店铺的url
    """

    def parse_info(self, response):
        data = json.loads(response.text)
        # print(data.keys())
        # print(data)
        code = data['code']
        url = response.meta['url']
        headers = response.meta['headers']

        if code != 200:
            # print(data)
            print(f'{url}异常，重新请求')
            yield scrapy.Request(url=url, headers=headers, callback=self.parse_info,
                                 meta={'url': url, 'headers': headers},
                                 dont_filter=True)
        else:
            from XCrawlSpider.items import XcrawlspiderItem
            item = XcrawlspiderItem()
            city = response.meta['city']
            mid_re = []

            reviewAllDOList = data['reviewAllDOList']
            for reviewDataVO in reviewAllDOList:
                # 评论体
                repl = reviewDataVO['reviewDataVO']['reviewData']['reviewBody']
                repl = re.sub('<svgmtsi class="review">', '', reviewDataVO['reviewDataVO']['reviewData']['reviewBody'])
                repl = re.sub('</svgmtsi>', '', repl)
                repl = re.sub(r'<br />', '', repl, re.DOTALL)
                repl = re.sub(r'<img class=".*?" src=".*?" alt=""/>', '', repl, re.DOTALL)
                repl = re.sub(r'&nbsp;', '', repl, re.DOTALL)
                # 遍历字典
                for key, value in self.review.items():
                    repl = repl.replace(key.replace('uni', '&#x') + ';', value)
                # print(repl)
                mid_re.append(repl)
            # 评论
            item['review'] = mid_re
            # 城市名称
            item['city'] = response.meta['city']
            # 城市url
            item['shop_url'] = response.meta['shop_url']

            print(f"{item['shop_url']}信息采集成功")
            time.sleep(random.randint(1, 3))
            yield item

    def get_token(self):
        with open('./js/rohr.min.js', 'r', encoding='utf-8') as fp:
            js = fp.read()

        JS = execjs.compile(js)
        token = JS.call("hhh_token", f'https://www.dianping.com?shopId={self.shop_id}')
        # print(token)
        return token
