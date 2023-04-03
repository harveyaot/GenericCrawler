# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

import pymongo


class RedditPipeline:
    def process_item(self, item, spider):
        return item

class RedditMongoPipeline:
    def __init__(self, mongo_uri, mongo_db, collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'),
            collection_name = crawler.settings.get('MONGO_COLLECTION_NAME')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # first check if insert before 
        cache = self.db[self.collection_name].find_one({'post_id':adapter.get('post_id')}, {'post_id': 1, '_id': 0})
        # check if needed update
        if cache:
            self.db[self.collection_name].update_one({'post_id':adapter.get('post_id')}, {"$set": adapter.asdict()})
        else: 
            self.db[self.collection_name].insert_one(adapter.asdict())
        return item
