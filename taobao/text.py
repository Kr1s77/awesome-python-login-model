# -*- coding: utf-8 -*-
import requests

# headers = {
#     'Connection': 'keep-alive',
#     'Host': 'item.taobao.com',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
# }
# url='https://item.taobao.com/item.htm?spm=a219r.lm874.14.1.422f2140YG82hc&id=574990577169&ns=1&abbucket=20#detail'
# # yield SplashRequest(page_url, self.parse1, args={'wait': 0.5}, splash_headers=self.headers, dont_filter=True)
# page=requests.get(url,headers=headers)
# print(page.text)
import re
# Start your middleware class
class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxy'] =self.proxy_test()

    def proxy_test(self):
        # ....
        def get_proxy():
            return requests.get("http://192.168.1.137:8001/get/").text

        def delete_proxy(proxy):
            requests.get("http://192.168.1.137:8001/delete/?proxy={}".format(proxy))

        proxy = "http://{}".format(get_proxy())
        try:
            requests.get('https://www.baidu.com', proxies={"proxy": proxy})
            print(proxy,'代理可用')
            # 使用代理访问
            return proxy
        except Exception:
            # 出错1次, 删除代理池中代理
            delete_proxy(proxy)
            return None

DOWNLOADER_MIDDLEWARES = {
   # 'taobao.middlewares.TaobaoDownloaderMiddleware': 543,
   'scrapy_splash.SplashCookiesMiddleware': 723,
   'scrapy_splash.SplashMiddleware': 725,
   'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
   'taobao.middlewares.ProxyMiddleware': 100,
}