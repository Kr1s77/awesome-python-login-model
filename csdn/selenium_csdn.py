# -*- coding: utf-8 -*-
# @Author: Kris
# @Mail: criselyj@163.com
# @Date:   2020-08-14 17:40:11
import os
import random
from getpass import getpass
import asyncio
from pyppeteer import launch


base_url = 'https://passport.csdn.net/login'
current_dir = os.path.dirname(os.path.realpath(__file__))
# Fix:https://github.com/miyakogi/pyppeteer/issues/183 文件权限问题。
cache_dir = os.path.join(current_dir, 'cache')
if not os.path.exists(cache_dir):
    os.mkdir(cache_dir)


class Api(object):
    def __init__(self, account, password):
        self.url = base_url
        self.account = account
        self.password = password
        self.browser = None
        self.page = None

    async def send_key(self):
        await asyncio.sleep(random.randint(2, 3))
        switch_btn = await self.page.xpath('//ul/li[@class="text-tab border-right"][2]/a')
        await switch_btn[0].click()
        input_account = await self.page.xpath('//div[@class="form-group"]/div/input[1]')
        await input_account[0].type(self.account,
                             {'delay': random.randint(100, 200) - 50})
        await self.page.type('#password-number', self.password,
                             {'delay': random.randint(100, 200) - 50})

        await self.page.click('button[data-type=account]')
        await asyncio.sleep(random.randint(5, 10))

    async def crawl(self):
        # 测试环境下 headless 设置为 False
        # 生产环境可以修改为无头浏览器
        self.browser = await launch({
            'headless': False,
            'userDataDir': cache_dir,
            'defaultViewport': {'width': 1440, 'height': 1000},
            'args': ['--no-sandbox']
        })
        self.page = await self.browser.newPage()
        await self.page.goto(self.url)

        # 伪造当前浏览状态 防止自动化工具检测
        codes = (
            "() =>{ Object.defineProperties(navigator,{ webdriver:"
            "{ get: () => false } }) }",
            "() =>{ window.navigator.chrome = { runtime: {},  }; }",
            "() =>{ Object.defineProperty(navigator, 'languages', "
            "{ get: () => ['en-US', 'en'] }); }",
            "() =>{ Object.defineProperty(navigator, 'plugins', { "
            "get: () => [1, 2, 3, 4, 5,6], }); }"
        )
        for code in codes:
            await self.page.evaluate(code)
        await self.send_key()


def main():
    print('[*] 模拟登陆 CSDN 程序启动...')
    account = input('[*] 请输入账号：')
    password = getpass('[*] 请输入密码：')
    login = Api(account, password)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(login.crawl())
    

if __name__ == '__main__':
    main()
