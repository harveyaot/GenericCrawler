# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import datetime

from scrapy.loader import ItemLoader
from ..items import OpinionNewsItem

class BloombergSpider(scrapy.Spider):
    name = "bloomberg"
    base_url = "https://www.bloomberg.com"
    allowed_domains = ['bloomberg.com']
    start_urls = [
        'https://www.bloomberg.com/opinion-technology-and-ideas',
        'https://www.bloomberg.com/opinion-business',
        'https://www.bloomberg.com/opinion-politics-and-policy',
        'https://www.bloomberg.com/opinion-economics'
        'https://www.bloomberg.com/opinion-markets',
        'https://www.bloomberg.com/opinion-finance'
    ]

    def parse(self, response):
        now = datetime.datetime.now()   
        nowTS = int(now.timestamp())

        """
        for article in response.xpath('//div[contains(@class, "styles_storyContainer")]'):
            title = article.xpath('.//div[contains(@data-component, "headline")]/a/text()').get()
            url = article.xpath('.//div[contains(@data-component, "headline")]/a/@href').get()
            summary = article.xpath('.//section[contains(@data-component, "summary")]/text()').get()
            imgs = article.xpath('.//img[contains(@data-component, "image")]/@srcset').get()
            thumbnail = imgs.split(",")[0].split(" ")[0]
            author = ''
        """
        for article in response.xpath('//article[contains(@class, "styles_article")]'):
            
            title = article.xpath('.//div[contains(@data-component, "headline")]/a/text()').get()
            # the legacy logic
            #summary = article.xpath('.//div[contains(@class, "summary")]/p/text()').get()
            #[TODO]
            summary = ''
            url = article.xpath('.//div[contains(@data-component, "headline")]/a/@href').get()
            imgs = article.xpath('.//img[contains(@data-component, "image")]/@srcset').get()
            thumbnail = imgs.split(",")[0].split(" ")[0]
            author = article.xpath('.//div[contains(@data-component, "byline")]/span/text()').get()
            
            yield OpinionNewsItem(title=title.strip('\n '), 
                                  summary=summary, 
                                  url=self.base_url + url, 
                                  thumbnail=thumbnail, 
                                  author=author,
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