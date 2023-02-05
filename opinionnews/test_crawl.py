import logging
import subprocess
import json
import os

# create folder name test if not exist
os.makedirs('test_output', exist_ok=True)

logger = logging.getLogger(__name__)
# logger add hander to file test_crawl.log in overwrite mode
logger.addHandler(logging.FileHandler('test_output/test_crawl.log', mode='w'))
logger.setLevel(logging.INFO)



spider_list = ['newsweek', 'foreignpolicy', 'bloomberg']

def run_crawls():
    for spider in spider_list:
        proc = subprocess.run(
            ["scrapy", "crawl", spider, "--overwrite-output", f"test_output/test_output_{spider}.json",
             "-s", "ITEM_PIPELINES={}"],
            stderr=subprocess.PIPE
        )
        stats_crawl_results(spider, f"test_output/test_output_{spider}.json")
        # verify the results
    

def stats_crawl_results(spider, json_output):
    # load the json_output, and test how many items were crawled,
    # stats how many titles, authors, url, thumbnais and summaries
    # within item are empty
    logger.info(f"\n=========[{spider}]=========")
    with open(json_output) as f:
        items = json.load(f)
        logger.info(f"Crawl stats information for {spider}")
        logger.info(f"Total items crawled: {len(items)}") 
        logger.info(f"Total items with  title: {len([item for item in items if item.get('title', None)])}")
        logger.info(f"Total items with  author: {len([item for item in items if item.get('author', None)])}")
        logger.info(f"Total items with  url: {len([item for item in items if item.get('url', None)])}")
        logger.info(f"Total items with  thumbnail: {len([item for item in items if item.get('thumbnail', None)])}")
        logger.info(f"Total items with  summary: {len([item for item in items if item.get('summary',None)])}")
        
run_crawls()
    

