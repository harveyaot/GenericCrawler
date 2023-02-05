import subprocess

spider_list = ['newsweek', 'foreignpolicy', 'bloomberg']

def run_crawls():
    for spider in spider_list:
        subprocess.run(
            ["scrapy", "crawl", spider],
        )
        
run_crawls()