<h2 align="center"><code>Website_login_mode</code></h2>

<br>
<p align="center">
    <img src="https://github.com/CriseLYJ/flask-video-streaming-recorder/blob/master/img/main.jpg?raw=true" 
        alt="Master">
</p>

<br>

<p align="center">"<i>Did you know all your doors were locked?</i>" - Riddick (The Chronicles of Riddick)</p>

<br>
<div align="center">
  <sub>Created by
  <a href="https://criselyj.github.io/">CriseLYJ</a>
</div>

<br>

****

# Website_login_mode
收集了一些各大网站登陆方式，有的是通过selenium登录，有的是通过抓包直接模拟登录，希望对小白有所帮助,本项目用于研究和分享各大网站的模拟登陆方式。

## 模拟登录一些常见的网站
主要基于以下的 Python 的第三 library 

1. requests
2. selenium 
3. rsa
4. phantomjs


## About

模拟登陆基本采用的是直接登录或者使用selenium+webdriver的方式，有的网站直接登录难度很大，比如qq空间，如果采用selenium就相对轻松一些。

虽然在登录的时候采用的是selenium,为了效率，我们可以在登录过后得到的cookie维护起来，然后调用requests或者scrapy等进行数据采集，这样数据采集的速度可以得到保证。

## Done

- [x] [Facebook](https://www.facebook.com/)
- [x] [无需身份验证即可抓取Twitter前端API](https://twitter.com/)
- [x] [微博网页版](http://weibo.com)
- [x] [知乎](http://zhihu.com)
- [x] [QQZone](https://qzone.qq.com/)
- [x] [CSDN](https://www.csdn.net/)
- [x] [淘宝](www.taobao.com)
- [x] [Baidu](www.baidu.com)
- [x] [果壳](https://www.guokr.com/)
- [x] [JingDong](https://www.jd.com/)
- [x] [163mail](https://mail.163.com/)
- [x] [拉钩](https://www.lagou.com/)
- [x] [Bilibili](https://www.bilibili.com/)
- [x] [豆瓣](https://www.douban.com/)
- [x] [V2EX](https://www.v2ex.com/)
- [x] [Baidu2](www.baidu.com)
- [x] [猎聘网](https://www.liepin.com/)
- [x] [微信网页版](https://wx.qq.com/)
- [x] [gihub](https://github.com/)
- [x] [图虫](https://tuchong.com/)

## show
- web微信
![Alt text](./image/weixin.jpg)

- 图虫爬虫

![](./image/Jietu20190306-232224.jpg)

![](./image/Jietu20190306-232303.jpg)

## tips of pull request 

- 欢迎大家一起来 pull request 

## Problems

- 关于验证码：本项目所用的方法都没有处理验证码，识别复杂验证码的难度就目前来说，还是比较大的。以我的心得来说，做爬虫最好的方式就是尽量规避验证码。
- 代码失效：由于网站策略或者样式改变，导致代码失效，请给我提issue，如果你已经解决，可以提PR，谢谢！

## Another
- 如果你有什么比较难登陆的网站，比如发现用了selenium+webdriver都还登陆不了的网站，欢迎给我提issue
- 如果该repo对大家有帮助，给个star鼓励鼓励吧

## something to add

1. 项目写了一段时间后，发现代码的风格和程序的易用性，可扩展性，代码的可读性，都存在一定的问题，所以接下来最重要的是重构代码，让大家可以更容易的做出一些自己的小功能。
2. 如果你觉得某个网站的登录很有代表性，欢迎在 issue 中提出
3. 如果网站的登录很有意思，我会在后面的更新中加入
4. 网站的登录机制有可能经常的变动，所以当现在的模拟的登录的规则不能使用的时候，请在 issue 中提出
- 如果关注量大的话，我还是会不断维护此仓库带来更多的东西，并且重构代码，

## Acknowledgement
- Thanks for all!

## Written at the end
- I need your support.
- And I think you can give me a ``star``!

