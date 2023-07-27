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
        
        for article in response.xpath('//article[contains(@class, "styles_article")]'):
            
            title = article.xpath('.//div[contains(@data-component, "headline")]/a/text()').get()
            # the legacy logic
            #summary = article.xpath('.//div[contains(@class, "summary")]/p/text()').get()
            #[TODO]
            summary = ''
            url = article.xpath('.//div[contains(@data-component, "headline")]/a/@href').get()
            thumbnail = article.xpath('.//img[contains(@data-component, "image")]/@src').get()
            author = article.xpath('.//div[contains(@data-component, "byline")]/span/text()').get()
            """
            url = response.xpath('//article[contains(@class, "article-story")]/div[contains(@class, "thumbnail")]/a/@href').getall()
thumbnail = response.xpath('//article[contains(@class, "article-story")]/div[contains(@class, "thumbnail")]//img/@src').getall()

title = response.xpath('//article[contains(@class, "article-story")]/div[contains(@class, "details")]//p/text()').getall()
            """
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