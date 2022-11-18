import json
import random
import time

import execjs
import scrapy
import pandas as pd
from fake_useragent import UserAgent
import re

# from XCrawlSpider.XCrawlSpider.items import XcrawlspiderItem


class CommentspiderSpider(scrapy.Spider):
    name = 'commentSpider'
    # allowed_domains = ['www.xxx.com']
    # start_urls = []

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
                # for urls in ['https://www.dianping.com/shop/G9X32n6EvRA5uwdp']:
                for urls in pds.iloc[:, 1].values:
                    self.shop_id = urls.split('/')[-1]
                    # print(self.shop_id)
                    headers = {
                        # 'Cookie': '_lxsdk_cuid=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _lxsdk=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _hc.v=7db62757-4617-03c5-8227-a3b30a9803c6.1666510368; s_ViewType=10; WEBDFPID=5w0830xz08w35yvu197y7429u76xy6u781596x519x997958zvww6ww3-1981870520158-1666510519831MQUYSAUfd79fef3d01d5e9aadc18ccd4d0c95077639; ctu=3eada7613bfd5549da00debc4ee9ff6190908a18a5ec7383aee478c9ff16b664; cy=1946; cye=bange; dper=de89a983a903d8800d8406b5e096b455290424d5cd5b889f9d0313532957c54f62516b79d73044ac32008348c20522b285b6d3a3a37fcca240e3362fe3d1ded7; ll=7fd06e815b796be3df069dec7836c3df; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1667380665,1667492509,1667796220,1667797032; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1667797079; _lxsdk_s=1845066b67b-9cb-592-a2b%7C%7C88',
                        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                        'User-Agent': UserAgent().random,
                        'Host': 'www.dianping.com',
                        'Referer': 'https://www.dianping.com/shop/{}'.format(self.shop_id),
                    }
                    url = f'https://www.dianping.com/ajax/json/shopDynamic/allReview?shopId={self.shop_id}&cityId=2372&shopType=10&tcv=gm10yk0jck&_token={self.get_token()}&uuid=9fec2d1c-9253-9f08-843d-4d8d0bd47aaa.1668095623&platform=1&partner=150&optimusCode=10&originUrl=https://www.dianping.com/shop/{self.shop_id}'
                    print(f"*******step 1:********\nshop_id:\t{self.shop_id}\nurl:\n{url}")
                    shop_url = urls
                    time.sleep(random.randint(1, 3))
                    yield scrapy.Request(url=url, headers=headers, callback=self.parse_info, meta={'url': url, 'headers': headers, 'city': city, 'shop_url': shop_url}, dont_filter=True)
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
            yield scrapy.Request(url=url, headers=headers, callback=self.parse_info, meta={'url': url, 'headers': headers},
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
                mid_re.append(repl)
            # 评论
            item['review'] = mid_re
            # 城市名称
            item['city'] = response.meta['city']
            # 城市url
            item['shop_url'] = response.meta['shop_url']

            print(f"{item['shop_url']}加密信息采集成功")
            time.sleep(random.randint(1, 3))
            headers = {
                'User-Agent': UserAgent().random,
                'Host': 'www.dianping.com',
            }
            yield scrapy.Request(url=item['shop_url'], headers=headers, callback=self.parse_css, meta={'url': url, 'headers': headers, 'item': item},
                                 dont_filter=True)

    """
        获取css的url
        callback: parse_css
        meta: 加密后的评论，城市名称，店铺的url
    """
    def parse_css(self, response):
        css_url = re.findall(r'<link rel="stylesheet" type="text/css" href="(.*?)">', response.text)
        print(f"*******step 2*********\ncss_list的长度为{len(css_url)}")
        print(f"css的详细url:{css_url[1]}")
        headers = {
            'User-Agent': UserAgent().random,
        }
        yield scrapy.Request(url='http:'+css_url[1], headers=headers, callback=self.parse_font,
                             meta={'item': response.meta['item']},
                             dont_filter=True)

    def parse_font(self, response):
        font_group = re.search(r'url\("(.*?)"\);} .review', response.text)
        font_url = 'http:' + font_group[1].split('"')[-1]
        print(f"*******step 3*********\n字体的url:{font_url}")
        # print("shop name的css url:", font_url)

    def parse(self, response, *args, **kwargs):
        pass
        # print('parse')
        # data = json.loads(response.text)
        # # print(data.keys())
        # # print(data)
        # code = data['code']
        # url = response.meta['url']
        # headers = {
        #     'User-Agent': UserAgent().random,
        #     'Host': 'www.dianping.com',
        # }
        # if code != 200:
        #     print(data)
        #     yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={'url': url, 'headers': headers}, dont_filter=True)
        # else:
        #     from XCrawlSpider.items import XcrawlspiderItem
        #     item = XcrawlspiderItem()
        #     city = response.meta['city']
        #     mid_re = []
        #
        #     reviewAllDOList = data['reviewAllDOList']
        #     for reviewDataVO in reviewAllDOList:
        #         # 评论体
        #         repl = reviewDataVO['reviewDataVO']['reviewData']['reviewBody']
        #         # print(repl)
        #         # print(repl)
        #         repl = re.sub('<svgmtsi class="review">', '', reviewDataVO['reviewDataVO']['reviewData']['reviewBody'])
        #         repl = re.sub('</svgmtsi>', '', repl)
        #         repl = re.sub(r'<br />', '', repl, re.DOTALL)
        #         repl = re.sub(r'<img class=".*?" src=".*?" alt=""/>', '', repl, re.DOTALL)
        #         repl = re.sub(r'&nbsp;', '', repl, re.DOTALL)
        #         mid_re.append(repl)
        #         # print(repl)
        #     # print(reviewAllDOList)
        #     # 评论
        #     item['review'] = mid_re
        #     # 城市名称
        #     item['city'] = response.meta['city']
        #     # 城市url
        #     item['shop_url'] = response.meta['shop_url']
        #     # print(mid_re)
        #     # item['shop_name'] = self.shop_name
        #     # with open('data.json', 'w', encoding='utf-8') as fp:
        #     #     json.dump(data, fp, ensure_ascii=False)
        #
        #     yield item

    def get_token(self):
        with open('./js/rohr.min.js', 'r', encoding='utf-8') as fp:
            js = fp.read()

        JS = execjs.compile(js)
        token = JS.call("hhh_token", f'https://www.dianping.com?shopId={self.shop_id}')
        # print(token)
        return token
