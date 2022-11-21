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
                self.shop_id = urls.split('/')[-1]
                # print(self.shop_id)
                cookie = [
                    """chrome"""
                    f's_ViewType=10; _lxsdk_cuid=18431b3e864c8-01933c488e725a-26021b51-384000-18431b3e864c8; _lxsdk=18431b3e864c8-01933c488e725a-26021b51-384000-18431b3e864c8; _hc.v=652bc9d6-1f70-3c7b-55b7-445886fd6498.1667281185; WEBDFPID=9y5708w5vu5059xv0u815u3519wx6y2881568y530zu979588v74z2vx-1982641217806-1667281217370SOQMUYYfd79fef3d01d5e9aadc18ccd4d0c95071750; ctu=3eada7613bfd5549da00debc4ee9ff61cf0c6fe7b9b663833fc2c67b06018752; fspop=test; cy={cy}; cye={cye}; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1668914644,1668918849,1668945415,1669007193; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1669007265; _lxsdk_s=1849894b2b2-936-b7b-1fe%7C%7C249',
                    """edge"""
                    f'_lxsdk_cuid=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _lxsdk=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _hc.v=9fec2d1c-9253-9f08-843d-4d8d0bd47aaa.1668095623; s_ViewType=10; fspop=test; cy={cy}; cye={cye}; __utma=205923334.1124010926.1668848108.1668848108.1668848108.1; __utmz=205923334.1668848108.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); WEBDFPID=8x7y7yz136w6589yz97u5zwy8z6x294v8151u8y12zx979588w9915xu-1984208257365-1668848257101QMIMWGKfd79fef3d01d5e9aadc18ccd4d0c95071406; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1668911845,1668918822,1668945215,1669003562; _lx_utm=utm_source=bing&utm_medium=organic; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1669004299; _lxsdk_s=184985d4d16-679-27-368%7C%7C58',
                    f'_lxsdk_cuid=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _lxsdk=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _hc.v=9fec2d1c-9253-9f08-843d-4d8d0bd47aaa.1668095623; s_ViewType=10; fspop=test; __utma=205923334.1124010926.1668848108.1668848108.1668848108.1; __utmz=205923334.1668848108.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); WEBDFPID=8x7y7yz136w6589yz97u5zwy8z6x294v8151u8y12zx979588w9915xu-1984208257365-1668848257101QMIMWGKfd79fef3d01d5e9aadc18ccd4d0c95071406; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1668911845,1668918822,1668945215,1669003562; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; cy=4; cye=guangzhou; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1669006636; _lxsdk_s=18498ab92ed-3c3-1ed-ba1%7C%7C1',
                ]
                headers = {
                    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                    'User-Agent': UserAgent().random,
                    'Host': 'www.dianping.com',
                    # 'Referer': 'https://www.dianping.com/shop/{}'.format(self.shop_id),
                    'Cookie': random.choice(cookie),
                    # 'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                    # 'sec-ch-ua-mobile': '?0',
                    # 'sec-ch-ua-platform': 'Windows',
                    # 'Sec-Fetch-Dest': 'document',
                    # 'Sec-Fetch-Mode': 'navigate',
                    # 'Sec-Fetch-Site': 'none',
                    # 'Sec-Fetch-User': '?1',
                    # 'Upgrade-Insecure-Requests': '1',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                    # 'Cache-Control': 'max-age=0',
                    # 'Connection': 'keep-alive',
                }
                # 获取十位时间戳
                timestamp = int(time.time())
                uuid = f'{random.randint(1, 9)}fec2d1c-9253-9f08-843d-4d8d0bd47aaa.{timestamp}'
                url = f'https://www.dianping.com/ajax/json/shopDynamic/allReview?shopId={self.shop_id}&cityId=2372&shopType=10&tcv=jo0yrd5tgg&_token={self.get_token()}&uuid={uuid}&platform=1&partner=150&optimusCode=10&originUrl=https://www.dianping.com/shop/{self.shop_id}'
                print(f"*******step 1:********\nshop_id:\t{self.shop_id}\nurl:\t{url}")
                shop_url = urls
                time.sleep(random.randint(1, 3))
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
            time.sleep(random.randint(10, 30))

            yield scrapy.Request(url=url, headers=headers, callback=self.parse_info,
                                 meta={'url': url, 'headers': headers},
                                 dont_filter=True)
        else:
            from XCrawlSpider.items import XcrawlspiderItem
            item = XcrawlspiderItem()
            # city = response.meta['city']
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
            yield item

    def get_token(self):
        with open('./js/rohr.min.js', 'r', encoding='utf-8') as fp:
            js = fp.read()

        JS = execjs.compile(js)
        token = JS.call("hhh_token", f'https://www.dianping.com?shopId={self.shop_id}')
        # print(token)
        return token
