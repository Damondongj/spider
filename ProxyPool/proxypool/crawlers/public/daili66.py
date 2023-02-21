from pyquery import PyQuery as pq 
from proxypool.schemas.Proxy import Proxy
from proxypool.crawler.base import BaseCrawler

BASE_URL = 'http://www.66ip.cn/{page}.html'
MAX_PAGE = 50

class Daili66Crawler(BaseCrawler):
    
    urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE+1)]
    
    def parse(self, html):
        doc = pq(html)
        # class 包含 containerbox 下面所有的 table 节点下面所有的 tr 节点, 选择索引大于0的节点
        # .items() 获取多节点
        trs = doc(".containerbox table tr:gt(0)").items()
        for tr in trs:
            # .find() 查找符合条件的所有子孙节点
            host = tr.find("td:nth-child(1)").text()
            port = int(tr.find("td:nth-child(2)").text())
            yield Proxy(host=host, port=port)

if __name__ == "__main__":
    crawler = Daili66Crawler()
    for proxy in crawler.crawl():
        print(proxy)