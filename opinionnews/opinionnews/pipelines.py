# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pymongo
import hashlib
import datetime
import json
import requests


class OpinionnewsFilterPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('title') is None:
            raise DropItem("Missing title")
        
        adapter['docid'] = hashlib.md5(adapter['url'].encode()).hexdigest()
        adapter['author'] = adapter['author'].strip().replace('By', '').strip('\n \t')
        return item

class OpinionNewsMongoPipeline:

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
        nowTS = int(datetime.datetime.now().timestamp())
        # first check if insert before 
        cache = self.db[self.collection_name].find_one({'docid':adapter.get('docid')}, {"title":1,"author":1,"summary":1})

        # check if needed update
        if cache:
            title = cache.get('title')
            author = cache.get('author')
            summary = cache.get('summary')

            # duplicated one no need after pipeline to run
            if adapter.get('title') == title and adapter.get('author') == author and adapter.get('summary') == summary:
                raise DropItem('duplicated one no need after pipeline to run')
            else:
                adapter['updateDate'] = nowTS 
                self.db[self.collection_name].update_one({'docid':adapter.get('docid')}, {"$set": adapter.asdict()})
                adapter['need_update'] = True
        else: 
            # insert new one
            adapter['firstDetectDate'] = nowTS
            self.db[self.collection_name].insert_one(adapter.asdict())
        return item

class OpinionNewsCMSPipeline:

    def __init__(self, api, api_token):
        self.api = api 
        self.request_headers = {"Content-Type": "application/json","Authorization": f"Bearer {api_token}"}

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            api = crawler.settings.get('CMS_API'),
            api_token = crawler.settings.get('CMS_API_TOKEN'),
        )

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        data = {'data': adapter.asdict()}
        nowStr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # handle update cases
        if adapter.get('need_update'):
            docid = adapter.get('docid')
            try:
                r = requests.get(self.api + f"?filters[docid][$eq]={docid}&fields[0]=id",
                                  headers = self.request_headers)
                d = r.json()
                cmsId = d['data'][0]['id']
                data['data']['updateDate'] = nowStr
                requests.put(self.api + f"/{cmsId}", headers=self.request_headers, data=json.dumps(data))
            except Exception as e:
                print(e)
                pass
        else:
            data['data']['firstDetectDate'] = nowStr
            requests.post(self.api, headers=self.request_headers, data=json.dumps(data))
        return item