import json
import random
import time

import execjs
import scrapy
import pandas as pd
from fake_useragent import UserAgent
import re

class ReviewhtmlSpider(scrapy.Spider):
    name = 'reviewHtml'
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
        city_log = pd.read_csv(path).iloc[:, 0].values
        log = pd.read_csv(path).iloc[:, 1].values
        log = pd.DataFrame(log, columns=['shop_url'])
        # print(city_list)
        for city in city_list:
            pds = pd.read_csv(f'./csv/{city}.csv').iloc[:, 1].values
            # numpy转为DataFrame
            df = pd.DataFrame(pds)
            # 去重
            df.drop_duplicates(inplace=True)
            # 删除两个DataFrame中相同的行
            pds = df[~df.isin(log)]
            print(pds)
            if city in city_log:
                print("已经爬取过")
            # if city not in city_log:
            cy = 57
            cye = 'alashan'
            print(pds)
            for urls in pds.iloc[:, 0].values:
                url = urls + '/review_all'
                # print(self.shop_id)
                headers = {
                    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                    'User-Agent': UserAgent().random,
                    'Host': 'www.dianping.com',
                    # 'Referer': 'https://www.dianping.com/shop/{}'.format(self.shop_id),
                    'Cookie': '_lxsdk_cuid=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _lxsdk=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _hc.v=9fec2d1c-9253-9f08-843d-4d8d0bd47aaa.1668095623; s_ViewType=10; fspop=test; __utma=205923334.1124010926.1668848108.1668848108.1668848108.1; __utmz=205923334.1668848108.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); WEBDFPID=8x7y7yz136w6589yz97u5zwy8z6x294v8151u8y12zx979588w9915xu-1984208257365-1668848257101QMIMWGKfd79fef3d01d5e9aadc18ccd4d0c95071406; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1668911845,1668918822,1668945215,1669003562; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; cy=4; cye=guangzhou; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1669022595; _lxsdk_s=18499718bf4-8d5-61-8e9%7C%7C491'
                }
                print(f"*******step 1:********\nurl:\t{url}")
                time.sleep(random.randint(1, 3))
                time.sleep(random.randint(1, 3))
                yield scrapy.Request(url=url, headers=headers, callback=self.parse_css,
                                     meta={'url': url, 'headers': headers, 'city': city},
                                     dont_filter=True)
                # yield scrapy.http.Request(url=url, headers=headers, callback=self.parse, meta={'url': url, 'headers': headers})

    def parse_css(self, response):
        fp = open('./index.html', 'w', encoding='utf-8')
        resp = response.text
        print(resp)
        # 正则表达式
        pattern = re.compile(r'<link rel="stylesheet" type="text/css" href="(.*?)">')
        # 匹配
        css_url = pattern.findall(resp)
        print(css_url)

        # print到文件
        print(resp, file=fp)
        # data = json.loads(response.text)
        # print(data.keys())
        # print(data)

        from XCrawlSpider.items import XcrawlspiderItem
        item = XcrawlspiderItem()
        # city = response.meta['city']
        mid_re = []
        # item['html'] = resp
        # # 评论
        # item['review'] = mid_re
        # # 城市名称
        # item['city'] = response.meta['city']
        # # 城市url
        # item['shop_url'] = response.meta['shop_url']

        # headers = {
        #     'User-Agent': UserAgent().random,
        #     'Host': 's3plus.meituan.net',
        # }
        # yield scrapy.Request(url=css_url, headers=headers, callback=self.parse_dict,
        #                      meta={'url': css_url, 'headers': headers, 'city': response.meta['city'], 'shop_url': response.meta['url'], 'html': resp},
        #                      dont_filter=True)

    def parse_dict(self, response, **kwargs):
        print(f"*******step 2:********\nurl:\t{response.url}")
        pass