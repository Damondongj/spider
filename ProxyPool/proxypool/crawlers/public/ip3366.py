from proxypool.crawler.base import BaseCrawler
from proxypool.schemas.Proxy import Proxy
import re
from bs4 import BeautifulSoup
from lxml import etree

MAX_PAGE = 3
BASE_URL = "http://www.ip3366.net/free/?stype={stype}&page={page}"


class Ip3366Crawler(BaseCrawler):
    
    urls = [BASE_URL.format(stype=stype, page=page) for stype in range(1, 10) for page in range(1, 20)]
    
    # def parse(self, html):
    #     soup = BeautifulSoup(html, "html.parser")
    #     trs = soup.select(".table-bordered tbody tr")
    #     for tr in trs:
    #         infos = list(tr.stripped_strings)
    #         host = infos[0].strip()
    #         port = int(infos[1].strip())
    #         yield Proxy(host=host, port=port)
    
    # def parse(self, html):
    #     # 
    #     ip_address = re.compile("<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>")
    #     re_ip_address = ip_address.findall(html)
    #     for address, port in re_ip_address:
    #         proxy = Proxy(host=address.strip(), port=int(port.strip()))
    #         yield proxy
    
    def parse(self, html):
        res = etree.HTML(html)
        # /html/body/div[3]/div[4]/table/tbody/tr[1]
        # trs = res.xpath('//div[@id="list"]/table/tbody/tr')
        trs = res.xpath('//*[@id="list"]/table/tbody/tr')
        for tr in trs:
            host = tr.xpath("./td[1]/text()")[0].strip()
            port = int(tr.xpath("./td[2]/text()")[0].strip())
            yield Proxy(host=host, port=port)
    
    def parse(self, html):
        import pandas as pd 
        df = pd.read_html(html, header=0)[0]
            
        def proxy_generate(arr):
            yield Proxy(host=arr["IP"].strip(), port=(arr["PORT"].strip()))
            
        # df.loc[:, ["IP", "PORT"]]  df.iloc[:, 0:2]
        # apply 函数 axis=1 的时候传入到函数里面的是行，axis=0的时候传入到函数里面的是列
        df[["IP", "PORT"]].apply(proxy_generate, axis=1)
            

if 1==1:
    crawler = Ip3366Crawler()
    for proxy in crawler.crawl():
        print(proxy)
            
        