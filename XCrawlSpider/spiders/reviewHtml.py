import json
import random
import time

import execjs
import scrapy
import pandas as pd
from fake_useragent import UserAgent
import re

from lxml import etree


class ReviewhtmlSpider(scrapy.Spider):
    name = 'reviewHtml'
    # allowed_domains = ['xxx.com']
    # start_urls = ['http://xxx.com/']

    def start_requests(self):
        fp = open('./css/background.css', 'r', encoding='utf-8')

        resp = fp.read()
        pattern = re.compile(r'\.(?P<tag>.*?)\{background:-(?P<x>.*?)px-(?P<y>.*?)px')
        self.result = pattern.finditer(resp)
        self.background = 'http:' + 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/c52c5f54f0f55645b6995aa1db09182b.svg'
        # self.background = 'http:' + re.findall(r'background-image:url(.*?)', resp)[0]

        # 读取json
        with open('./json/city_list.json', 'r', encoding='utf-8') as fp:
            data = json.load(fp)

        # with open('XCrawlSpider/spiders/json/review.json', 'r', encoding='utf-8') as fp:
        #     self.review = json.load(fp)

        city_list = data.keys()
        # print(city_list)
        # city_list = ['三亚']
        # 读取csv
        path = r'./log.csv'
        city_log = pd.read_csv(path).iloc[:, 0].values
        log = pd.read_csv(path).iloc[:, 1].values
        log = pd.DataFrame(log, columns=['shop_url'])


        result = pattern.findall(resp)
        print(result)
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
            for urls in pds.iloc[:, 0].values:
                url = urls + '/review_all'
                # print(self.shop_id)
                headers = {
                    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                    'User-Agent': UserAgent().random,
                    'Host': 'www.dianping.com',
                    'Cookie': '_lxsdk_cuid=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _lxsdk=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _hc.v=9fec2d1c-9253-9f08-843d-4d8d0bd47aaa.1668095623; s_ViewType=10; fspop=test; __utma=205923334.1124010926.1668848108.1668848108.1668848108.1; __utmz=205923334.1668848108.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); WEBDFPID=8x7y7yz136w6589yz97u5zwy8z6x294v8151u8y12zx979588w9915xu-1984208257365-1668848257101QMIMWGKfd79fef3d01d5e9aadc18ccd4d0c95071406; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; cy=4; cye=guangzhou; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1668918822,1668945215,1669003562,1669080037; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1669082774; _lxsdk_s=1849cec2e9e-6f7-26d-0f5%7C%7C414'
                }
                print(f"step 1:\nurl:\t{url}")
                time.sleep(random.randint(1, 6))
                time.sleep(random.randint(1, 6))
                yield scrapy.Request(url='https://www.baidu.com', headers=headers, callback=self.parse_css,
                                     meta={'url': url, 'headers': headers, 'city': city},
                                     dont_filter=True)
                # yield scrapy.http.Request(url=url, headers=headers, callback=self.parse, meta={'url': url, 'headers': headers})

    def parse_css(self, response):
        print(f"step 2:\nurl:\t{response.url}")

        # data = json.loads(response.text)
        # print(data.keys())
        # print(data)
        #
        # from XCrawlSpider.items import XcrawlspiderItem
        # item = XcrawlspiderItem()
        # # city = response.meta['city']
        # mid_re = []
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

if __name__ == '__main__':
    fp = open('../../css/background.css', 'r', encoding='utf-8')

    resp = fp.read()
    pattern = re.compile(r'\.(?P<tag>.*?)\{background:-(?P<x>.*?)px-(?P<y>.*?)px')
    result = pattern.finditer(resp)
    for groups in result:
        print(groups.group('tag'), groups.group('x'), groups.group('y'))