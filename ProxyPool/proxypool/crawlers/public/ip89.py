import re 
from proxypool.schemas.Proxy import Proxy
from proxypool.crawler.base import BaseCrawler


MAX_NUM = 9999
BASE_URL = 'http://api.89ip.cn/tqdl.html?api=1&num={MAX_NUM}&port=&address=&isp='.format(MAX_NUM=MAX_NUM)


class Ip89Crawler(BaseCrawler):
    
    urls = [BASE_URL]
    
    def parse(self, html):
        ip_address = re.compile("([\d:\.]*)<br>")
        hosts_ports = ip_address.findall(html)
        for addr in hosts_ports:
            addr_split = addr.split(":")
            if len(addr_split) == 2:
                host = addr_split[0]
                port = addr_split[1]
                yield Proxy(host=host, port=port)
                
if 1==1:
    crawler = Ip89Crawler()
    for proxy in crawler.crawl():
        print(proxy)