# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class OpinionNewsItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    thumbnail = scrapy.Field()
    author = scrapy.Field()
    authorDesc = scrapy.Field()
    summary = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    crawlDate = scrapy.Field(serializer=int) 

    publishDate = scrapy.Field()
    text = scrapy.Field()
    """
    title: str
    thumbnail: str
    author: str
    authorDesc: str
    summary: str
    source: str
    url: str
    crawlDate: str

    text: str
    publishDate: str
    """
    
