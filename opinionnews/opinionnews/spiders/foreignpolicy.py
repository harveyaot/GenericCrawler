# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import datetime

from scrapy.loader import ItemLoader
from ..items import OpinionNewsItem

class ForeignPolicySpider(scrapy.Spider):
    name = "foreignpolicy"
    allowed_domains = ['foreignpolicy.com']
    start_urls = [
        'https://foreignpolicy.com/channel/analysis/',
    ]

    def parse(self, response):
        now = datetime.datetime.now()
        nowTS = int(now.timestamp())
        
        for article in response.xpath('//div[contains(@class, "content-block")]'):
            title = article.xpath('.//h3/text()').get()
            summary = article.xpath('.//p[contains(@class, "dek")]/text()').get()
            url = article.xpath('.//div[contains(@class, "list-text")]/a/@href').get()
            thumbnail = article.xpath('./figure/a/img/@data-src').get()
            author = article.xpath('.//div[contains(@class, "list-text")]//address/a/text()').get()
            authorLink = article.xpath('.//div[contains(@class, "list-text")]//address/a/@href').get()
            """
            l = ItemLoader(item=OpinionNewsItem(), response=response)
            l.add_xpath('title', './/h3/a/text()')
            l.add_xpath('summary', './/div[contains(@class, "summary")]/text()')
            l.add_xpath('url', './/div[contains(@class, "image")]/a/@href')
            l.add_xpath('thumbnail', './/div[contains(@class, "image")]//picture/source/@data-srcset')
            l.add_xpath('author', './/div[contains(@class, "byline")]/text()')
            """
            yield OpinionNewsItem(title=title.strip('\n '), 
                                  summary=summary, 
                                  url=url, 
                                  thumbnail=thumbnail, 
                                  author=author,
                                  authorLink=authorLink,
                                  source=self.name,
                                  updateDate=nowTS)
            #yield {"title": title, 
            #       "summary": summary, 
            #       "url": url, 
            #       "thumbnail": thumbnail, 
            #       "author": author, 
            #       "crawlDate": nowTS}
            #item = l.load_item()
            #item.crawlDate = nowTS
            #yield item