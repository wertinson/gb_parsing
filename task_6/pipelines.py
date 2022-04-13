# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy1803

    def process_item(self, item, spider):
        print()
        # Обработка данных
        if spider.name == 'sjru':
            pass
        else:
            pass

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item
