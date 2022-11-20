import scrapy
import json
import random
import time

import execjs
import scrapy
import pandas as pd
from fake_useragent import UserAgent
import re

class ReviewSpider(scrapy.Spider):
    name = 'review'
    # allowed_domains = ['xxx.com']
    # start_urls = ['http://xxx.com/']

    def start_requests(self):
        # 读取json
        with open('./json/city_list.json', 'r', encoding='utf-8') as fp:
            data = json.load(fp)

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
                print(city)
                # for urls in ['https://www.dianping.com/shop/G9X32n6EvRA5uwdp']:
                for urls in pds.iloc[:, 1].values:
                    self.shop_id = urls.split('/')[-1]
                    # print(self.shop_id)
                    headers = {
                        'User-Agent': UserAgent().random,
                        'Host': 'www.dianping.com',
                    }
                    url = f'http://www.dianping.com/shop/{self.shop_id}/review_all/p1'
                    # url = f'https://www.dianping.com/ajax/json/shopDynamic/allReview?shopId={self.shop_id}&cityId=3577&shopType=10&tcv=gm10yk0jck&_token={self.get_token()}&uuid=9fec2d1c-9253-9f08-843d-4d8d0bd47aaa.1668095623&platform=1&partner=150&optimusCode=10&originUrl=https://www.dianping.com/shop/{self.shop_id}'
                    print(f"*******step 1:********\nshop_id:\t{self.shop_id}")
                    print(f'url:\t{url}')
                    shop_url = urls
                    time.sleep(random.randint(1, 3))
                    yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={'url': url, 'headers': headers, 'city': city, 'shop_url': shop_url}, dont_filter=True)
                    # yield scrapy.http.Request(url=url, headers=headers, callback=self.parse, meta={'url': url, 'headers': headers})

    def parse(self, response, *args, **kwargs):
        data = response.text
        # data = json.loads(response.text)
        # print(data.keys())
        # print(data)
        url = response.meta['url']
        headers = {
            'User-Agent': UserAgent().random,
            'Host': 'www.dianping.com',
        }
        if code != 200:
            print(data)
            yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={'url': url, 'headers': headers}, dont_filter=True)
        else:
            from XCrawlSpider.items import XcrawlspiderItem
            item = XcrawlspiderItem()
            city = response.meta['city']
            mid_re = []

            reviewAllDOList = data['reviewAllDOList']
            for reviewDataVO in reviewAllDOList:
                # 评论体
                # repl = reviewDataVO['reviewDataVO']['reviewData']['reviewBody']
                # print(repl)
                # print(repl)
                repl = re.sub('<svgmtsi class="review">', '', reviewDataVO['reviewDataVO']['reviewData']['reviewBody'])
                repl = re.sub('</svgmtsi>', '', repl)
                repl = re.sub(r'<br />', '', repl, re.DOTALL)
                repl = re.sub(r'<img class=".*?" src=".*?" alt=""/>', '', repl, re.DOTALL)
                repl = re.sub(r'&nbsp;', '', repl, re.DOTALL)
                mid_re.append(repl)
                # print(repl)
            # print(reviewAllDOList)
            # 评论
            item['review'] = mid_re
            # 城市名称
            item['city'] = response.meta['city']
            # 城市url
            item['shop_url'] = response.meta['shop_url']
            fp = open('./XCrawlSpider/spiders/json/review.json', 'r', encoding='utf-8')
            kv = json.load(fp)
            # print(kv.keys())
            for k in kv.keys():
                key = k.replace('uni', '&#x') + ';'
                for idx in range(len(item['review'])):
                    item['review'][idx] = item['review'][idx].replace(key, kv[k])
                    print(item['review'][idx])
            # print(item['review'])
            # print(mid_re)
            # item['shop_name'] = self.shop_name
            # with open('data.json', 'w', encoding='utf-8') as fp:
            #     json.dump(data, fp, ensure_ascii=False)

            # yield item
