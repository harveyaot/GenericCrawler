# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RedditItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # define a item based on this dictionary example:
    post_id = scrapy.Field()
    title = scrapy.Field()
    perm_link = scrapy.Field()
    source_url = scrapy.Field()
    preview = scrapy.Field()
    upvotes = scrapy.Field()
    comments = scrapy.Field()
    theme = scrapy.Field()
    sort = scrapy.Field()
    created = scrapy.Field()
    updated = scrapy.Field()
    author = scrapy.Field()
