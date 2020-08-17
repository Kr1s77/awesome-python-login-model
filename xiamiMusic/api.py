# -*- coding: utf-8 -*-
# @Author: Kris
# @Mail: criselyj@163.com
# @Date:   2020-08-14 17:40:11
import os
import random
import asyncio
from pyppeteer import launch

base_url = 'https://passport.xiami.com/'
current_dir = os.path.dirname(os.path.realpath(__file__))
# Fix:https://github.com/miyakogi/pyppeteer/issues/183 文件权限问题。
cache_dir = os.path.join(current_dir, 'cache')
if not os.path.exists(cache_dir):
    os.mkdir(cache_dir)


class XMLogin(object):
    url = base_url

    def __init__(self, account, password):
        self.account = account
        self.password = password
        self.browser = None
        self.page = None

    async def send_key(self):
        await self.page.click('.login-switch')
        await self.page.type('#account', self.account,
                             {'delay': random.randint(100, 200) - 50})
        await self.page.type('#password', self.password,
                             {'delay': random.randint(100, 200) - 50})

    async def slide(self):
        try:
            await self.page.hover('#captcha')
            await self.page.mouse.down()
            await self.page.mouse.move(2000, 0,
                                       {'delay': random.randint(2000, 4000)})
            await self.page.mouse.up()
        except Exception as e:
            print('error', e)
            exit(0)

    async def validate(self):
        try:
            error_element = await self.page.xpath('//div[@id="error"]')
            msg = await (
                await error_element[0].getProperty('textContent')).jsonValue()
        except Exception:
            return None
        return msg

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
        await asyncio.sleep(random.randint(2, 3))
        await self.slide()

        # 登录
        await asyncio.sleep(random.randint(2, 3))
        await self.page.click('#submit')
        msg = await self.validate()
        if msg:
            print('[*] 错误信息：', msg)
            exit(0)
        print('[*] 登录成功')
        await asyncio.sleep(5)


def main():
    print('[*] 模拟登陆虾米音乐程序启动...')
    account = input('[*] 请输入账号：')
    password = input('[*] 请输入密码：')
    login = XMLogin(account, password)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(login.crawl())


if __name__ == '__main__':
    main()
