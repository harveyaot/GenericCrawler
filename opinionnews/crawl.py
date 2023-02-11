import subprocess

spider_list = ['newsweek', 'foreignpolicy', 'bloomberg', 'scmp']

def run_crawls():
    for spider in spider_list:
        subprocess.run(
            ["scrapy", "crawl", spider],
        )
        
run_crawls()