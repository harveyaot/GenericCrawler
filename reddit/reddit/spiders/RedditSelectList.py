import scrapy
import datetime

from ..items import RedditItem


class RedditselectlistSpider(scrapy.Spider):
    name = 'RedditSelectList'
    allowed_domains = ['reddit.com']

    # read urls from external file urls.txt and add to start_urls:
    def start_requests(self):
        with open('urls.txt') as f:
            urls = [url.strip() for url in f.readlines()]
        
        reddit_api = "https://gateway.reddit.com/desktopapi/v1/subreddits"
        params = {
            "Rtj" : "only",
            "RedditWebClient" : "web2x&app=web2x-client-production",
            "AllowOver18" : "1",
            "Include": "identity",
            "Layout" : "card"
        }
        
        for url in urls:
            theme, sort = url.split('/')[-2:]
            if sort != 'new':
                params['Sort'] = sort
                crawl_url = f"{reddit_api}/{theme}?{params}" 
                yield scrapy.Request(url=crawl_url, callback=self.parse, meta={'theme': 'theme', 'sort': 'sort'})

    def parse(self, response):
        # get response json
        data = response.json()
        theme = response.meta['theme']
        sort = response.meta['sort']

        # parse the posts cards within the response
        for id, post in data['posts'].items():
            # skip posts that are not articles
            if post.get('isSponsored', False) or post.get('isNSFW',False) or post.get('isOriginalContent', False):
                continue
            
            if post.get('title', None) is None:
                continue
            try:
                yield RedditItem(
                    post_id = post['postId'],
                    title = post['title'],
                    preview = post['preview']['url'] if post.get('preview', False) else None,
                    perm_link = post['permalink'],
                    source_url = post['source']['url'] if post.get('source', False) else None,
                    upvotes = post['upvoteRatio'],
                    comments = post['numComments'],
                    theme = theme,
                    sort = sort,
                    created = post['created'],
                    updated = datetime.datetime.now(),
                    author = post['author']
                )
            except Exception as e:
                continue