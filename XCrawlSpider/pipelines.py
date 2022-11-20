# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class XcrawlspiderPipeline:
    def process_item(self, item, spider):
        review = item['review']
        city = item['city']
        shop_url = item['shop_url']
        print(review, city, shop_url)
        # pandas写入csv
        import pandas as pd
        df = pd.DataFrame({'city': city, 'shop_url': shop_url, 'review': review})
        df.to_csv(f'./reviews/{city}.csv', mode='a', index=False, header=False, encoding='utf-8-sig')
        # print(review)
        return item

class LogPipeline:
    def process_item(self, item, spider):
        # pandas写入csv
        import pandas as pd
        df = pd.DataFrame({'city': item['city'], 'shop_url': item['shop_url']}, index=[0])
        df.to_csv('./log.csv', mode='a', index=False, header=False, encoding='utf-8-sig')
        # print(review)
        print(item)
        return item

