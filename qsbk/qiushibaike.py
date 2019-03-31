# !/usr/bin/python3
# -*- coding: utf-8 -*-

# 1. 导入线程池模块
# 线程池
import gevent.monkey
gevent.monkey.patch_all()
from gevent.pool import Pool
from queue import Queue
import requests
from lxml import etree

class QiushiSpider():

    def __init__(self, max_page):
        self.max_page = max_page
        # 2. 创建线程池，初始化线程数量
        self.pool = Pool(5)

        self.base_url = "http://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }

        # 专门存放 url 容器
        self.url_queue = Queue()
        pass

    def get_url_list(self):
        '''
        获取 url 列表放入到 url 容器中
        :return:
        '''
        for page in range(1,self.max_page,1):
            url = self.base_url.format(page)
            self.url_queue.put(url)

    # 3. 实现执行任务
    def exec_task(self):
        # 1> 获取url
        url = self.url_queue.get()

        # 2> 发送请求获取 html
        response = requests.get(url,headers=self.headers)
        html = response.text

        # 3> 解析 html 提取数据
        eroot = etree.HTML(html)

        titles = eroot.xpath('//a[@class="recmd-content"]/text()')
        for title in titles:
            item = {}
            item["title"] = title

            # 4> 保存数据
            print(item)
        self.url_queue.task_done()



    # 4. 实现执行任务完成后的操作,必须至少有一个参数
    # result 任务执行的最终结果的返回值
    def exec_task_finished(self,result):
        print("result:",result)
        print("执行任务完成")
        self.pool.apply_async(self.exec_task,callback=self.exec_task_finished)


    def run(self):

        self.get_url_list()

        # 5. 让任务使用线程池中的线程执行并且设置执行后的回调操作
        # callback 表示执行完成后的回调
        for i in range(5):
            self.pool.apply_async(self.exec_task,callback=self.exec_task_finished)
        self.url_queue.join()
        pass

if __name__ == '__main__':
    max_page = input("请输入您需要多少页内容：")
    spider = QiushiSpider(int(max_page))
    spider.run()
