# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import execjs
import requests
from fake_useragent import UserAgent
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse


# class XcrawlspiderSpiderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, or item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Request or item objects.
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)


class XcrawlspiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     # This method is used by Scrapy to create your spiders.
    #     s = cls()
    #     crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
    #     return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        url_list = spider.start_urls
        print(url_list)
        if request.url in url_list:
            self.shop_id = request.url.split('/')[-1]
            print(self.shop_id)

            headers = {
                'Cookie': 'fspop=test; cy=153; cye=rizhao; _lxsdk_cuid=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _lxsdk=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _hc.v=7db62757-4617-03c5-8227-a3b30a9803c6.1666510368; s_ViewType=10; WEBDFPID=5w0830xz08w35yvu197y7429u76xy6u781596x519x997958zvww6ww3-1981870520158-1666510519831MQUYSAUfd79fef3d01d5e9aadc18ccd4d0c95077639; dper=ab7eef6129a412b25b0ac3854ff9e3bd0bf35371e8df4c10679b2f4ae332c4520bd2d188510101887353e78941e52b4a8a57ffa532d2ed4c662b55acd1dda1b993627620ed1e01619351ee224709f7c84571b76e4d9481e5692247f0803176e1; ua=dpuser_3830243167; ctu=3eada7613bfd5549da00debc4ee9ff6190908a18a5ec7383aee478c9ff16b664; _lx_utm=utm_source=bing&utm_medium=organic; ll=7fd06e815b796be3df069dec7836c3df; dplet=a1ded827ad67a2f1eaf855c2d2249de0; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666950926,1666995148,1667001764,1667098148; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1667099170; _lxsdk_s=18426cafb66-ae0-e72-2ab||121',
                'User-Agent': UserAgent().random,
                'Host': 'www.dianping.com',
                'Referer': 'https://www.dianping.com/shop/{}'.format(self.shop_id),
            }
            url = 'https://www.dianping.com/ajax/json/shopDynamic/allReview?shopId={}&cityId=8&shopType=10&tcv=4e7hqrxmfg&_token={}&uuid=7db62757-4617-03c5-8227-a3b30a9803c6.1666510368&platform=1&partner=150&optimusCode=10&originUrl=https://www.dianping.com/shop/l2g0kxUJRpV1bdZr'.format(
                self.shop_id, self.get_token())
            new_response = HtmlResponse(url=url, encoding='utf-8',headers=headers, request=request)
            return new_response
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def get_token(self):
        with open('./js/rohr.min.js', 'r', encoding='utf-8') as fp:
            js = fp.read()

        JS = execjs.compile(js)
        token = JS.call("hhh_token", 'https://www.dianping.com?shopId={}'.format(self.shop_id))
        return token

    #
    # def process_exception(self, request, exception, spider):
    #     # Called when a download handler or a process_request()
    #     # (from other downloader middleware) raises an exception.
    #     # Must either:
    #     # - return None: continue processing this exception
    #     # - return a Response object: stops process_exception() chain
    #     # - return a Request object: stops process_exception() chain
    #     pass
    #
    # def spider_opened(self, spider):
    #     spider.logger.info('Spider opened: %s' % spider.name)
