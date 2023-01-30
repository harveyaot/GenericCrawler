# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import datetime

from scrapy.loader import ItemLoader
from ..items import OpinionNewsItem

class NewsWeekSpider(scrapy.Spider):
    name = "newsweek"
    allowed_domains = ['newsweek.com']
    start_urls = [
        'https://newsweek.com/opinion',
    ]

    def parse(self, response):
        now = datetime.datetime.now()
        nowStr = now.strftime("%Y-%m-%d-%H")
        nowTS = int(now.timestamp())
        
        for article in response.xpath('//article'):
            title = article.xpath('.//h3/a/text()').get()
            # try another xpath if the first one fails
            if title is None:
                title = article.xpath('.//h6/a/text()').get()
            
            if title is not None:
                # replace the ending string "| Opinoin"
                title = title.replace("| Opinion", "").strip()
                    
            summary = article.xpath('.//div[contains(@class, "summary")]/text()').get()
            url = article.xpath('.//div[contains(@class, "image")]/a/@href').get()
            thumbnail = article.xpath('.//div[contains(@class, "image")]//picture/source/@data-srcset').get()
            author = article.xpath('.//div[contains(@class, "byline")]/text()').get()
            """
            l = ItemLoader(item=OpinionNewsItem(), response=response)
            l.add_xpath('title', './/h3/a/text()')
            l.add_xpath('summary', './/div[contains(@class, "summary")]/text()')
            l.add_xpath('url', './/div[contains(@class, "image")]/a/@href')
            l.add_xpath('thumbnail', './/div[contains(@class, "image")]//picture/source/@data-srcset')
            l.add_xpath('author', './/div[contains(@class, "byline")]/text()')
            """
            yield OpinionNewsItem(title = title, 
                                  summary = summary, 
                                  url = "https://www.newsweek.com" + url, 
                                  thumbnail = thumbnail.split(' ')[0], # hack 
                                  author = author,
                                  source = self.name,
                                  updateDate = nowTS)
            #yield {"title": title, 
            #       "summary": summary, 
            #       "url": url, 
            #       "thumbnail": thumbnail, 
            #       "author": author, 
            #       "crawlDate": nowTS}
            #item = l.load_item()
            #item.crawlDate = nowTS #yield item