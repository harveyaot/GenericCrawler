# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import datetime
import json

from scrapy.loader import ItemLoader
from ..items import OpinionNewsItem

class BloombergSpider(scrapy.Spider):
    name = "scmp"
    base_url = "https://www.scmp.com"
    allowed_domains = ['scmp.com']
    start_urls = [
        'https://www.scmp.com/comment/insight-opinion'
    ]

    def parse(self, response):
        now = datetime.datetime.now()
        nowTS = int(now.timestamp())

        # parse the script:
        script = response.xpath('//script[contains(., "window.__APOLLO_STATE__=")]/text()').get()
        print(script[:30])
        with open("scmp.json", "w") as f:
            f.write(script.replace("window.__APOLLO_STATE__=", ""))

        d = json.loads(script.replace("window.__APOLLO_STATE__=", ""))

        qs_opinions = []
        if "contentService" in d:
            for qs in d["contentService"].keys():
                if "opinion" in qs:
                    qs_opinions.append(qs)

        for qs in qs_opinions:
            val = d["contentService"][qs]
            if val.get("__typename", None) != "Article":
                continue

            url = val.get("urlAlias", "")
            title = val.get("headline", "")
            subHeadline = val.get("socialHeadline", "")
            updateDate = int(val.get("updatedDate",0) / 1000)
            if updateDate == 0:
                updateDate = nowTS
                

            # process image
            image = ""
            imgs = val.get("images", [])
            if imgs:
                id = imgs[0].get("id", None)
                if id and id in d["contentService"]:
                    image = d["contentService"][id]['url']
                    
            # process author
            authors = val.get("authors", []) 
            author, authorLink = "", ""
            id = authors[0].get("id", None)
            if id and id in d["contentService"]:
                author = d["contentService"][id]['name']
                authorLink = d["contentService"][id]['urlAlias']

            #  process summary
            
            summary = val.get("summary", {})
            ps = []
            if "json" in summary:
                for p in summary["json"]:
                    if p["type"] == "p":
                        ps.extend([c["data"] for c in p["children"]])
            ps.insert(0, subHeadline)
            summary = ". ".join(ps)

            yield OpinionNewsItem(title=title.strip('\n '), 
                                  summary=summary, 
                                  url=self.base_url + url, 
                                  thumbnail=image, 
                                  author=author,
                                  authorLink=authorLink,
                                  source=self.name,
                                  updateDate=updateDate)