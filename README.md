<h2 align="center"><code>🎉Life is fantastic🥳!~</code></h2>

<br>
<p align="center">
    <img src="https://github.com/CriseLYJ/flask-video-streaming-recorder/blob/master/img/main.jpg?raw=true" 
        alt="Master">
</p>

<br>

<p align="center">"<i>Did you know all your doors were locked?</i>" - Riddick (The Chronicles of Riddick)</p>
<br>

<p align="center">
  <a href="https://github.com/CriseLYJ/awesome-python-login-model/tree/master">
    <img src="https://img.shields.io/badge/Branch-master-green.svg?longCache=true"
        alt="Branch">
  </a>
  <a href="https://github.com/CriseLYJ/awesome-python-login-model/stargazers">
    <img src="https://img.shields.io/github/stars/CriseLYJ/awesome-python-login-model.svg?label=Stars&style=social"
        alt="Stars">
  </a>
    <a href="https://github.com/CriseLYJ/awesome-python-login-model/network/members">
    <img src="https://img.shields.io/github/forks/CriseLYJ/awesome-python-login-model.svg?label=Forks&style=social"
        alt="Forks">
  </a>
  <a href="http://www.gnu.org/licenses/">
    <img src="https://img.shields.io/badge/License-GNU-blue.svg?longCache=true"
        alt="License">
  </a>
   <a href="https://github.com/sindresorhus/awesome">
   <img src="https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg"
        alt="Awesome">
  </a>
</p>
<br>
<div align="center">
  <sub>Created by
  <a href="https://criselyj.github.io/">CriseLYJ</a>
</div>

<br>

****

# 💕Website login model
🌟收集了一些各大网站登陆方式， 和一些网站的爬虫程序，有的是通过selenium登录，有的是通过抓包直接模拟登录，有的是利用scrapy,希望对小白有所帮助,本项目用于研究和分享各大网站的模拟登陆方式，和爬虫程序，会持续更新。。。

## About

模拟登陆基本采用的是直接登录或者使用selenium+webdriver的方式，有的网站直接登录难度很大，比如qq空间，bilibili等如果采用selenium就相对轻松一些。

虽然在登录的时候采用的是selenium,为了效率，我们可以在登录过后得到的cookie维护起来，然后调用requests或者scrapy等进行数据采集，这样数据采集的速度可以得到保证。


## Completed

- [x] [Facebook](https://www.facebook.com/)
- [x] [无需身份验证即可抓取Twitter前端API](https://twitter.com/)
- [x] [微博网页版](http://weibo.com)
- [x] [知乎](http://zhihu.com)
- [x] [QQZone](https://qzone.qq.com/)
- [x] [CSDN](https://www.csdn.net/)
- [x] [淘宝](www.taobao.com)
- [x] [Baidu](www.baidu.com)
- [x] [果壳](https://www.guokr.com/)
- [x] [JingDong 模拟登录和自动申请京东试用](https://www.jd.com/)
- [x] [163mail](https://mail.163.com/)
- [x] [拉钩](https://www.lagou.com/)
- [x] [Bilibili](https://www.bilibili.com/)
- [x] [豆瓣](https://www.douban.com/)
- [x] [Baidu2](www.baidu.com)
- [x] [猎聘网](https://www.liepin.com/)
- [x] [微信网页版登录并获取好友列表](https://wx.qq.com/)
- [x] [Github](https://github.com/)
- [x] [爬取图虫相应的图片](https://tuchong.com/)
- [x] [网易云音乐](https://music.163.com/)
- [x] [糗事百科](https://www.qiushibaike.com/)

## show

### Bilibili自动登录测试正常，成功率98%

![](./images/bilibili.gif)

![](./images/bilibili.jpg)

### web微信

![](./images/weixin.gif)

![Alt text](./images/weixin.jpg)

### 图虫Spider

![](./images/tuchong.gif)

![](./images/tuchong.jpg)

### 淘宝web
- taobao.py为模拟登录
- 剩下的文件为爬虫

### Github

![](./images/github.jpg)

### 新增链家Spider

![](./images/lianjia.gif)

```
1. 爬取淘宝各子标签，按销量排名商品信息，按分类保存至MongoDB
2. 通过pandas进行数据分析
3 .将商品在各省分布、销量排行、地图分布等通过matplotlib绘图显示
```

### guoke.spider使用需谨慎，下载的比较快！10秒能下载一堆，截图我就不展示了，已经删除,东西太多了😝

### 微博
- sina.py为模拟登录
- spider文件夹中为爬虫

```
1. 输入要爬取的博主ID，获取ajax请求
2. 解析json数据，爬取博主所有微博，保存至MySQL

```

### 网易云音乐
- 新增网易云音乐下载，之前的一个小demo应该还可以用，Crypto包应该挺难搞的，安装之后还是导入不了，推荐去百度一下，百度上的这个解决方法有很多，我就不多赘述了嘿嘿！

### 知乎
- 知乎登录没有问题，不过要手动输入验证码

- 知乎登录遇到“execjs._exceptions.ProgramError: TypeError: 'exports' 未定义”
- 原因以及解决办法：
```
1. 由于是你本地的JScript引擎只有一个默认的JScript，所以会造成json未定义的错误。
2. execjs会自动使用当前电脑上的运行时环境
3. 解决办法：安装一个nodejs的V8引擎就可以了
```

![](./images/zhihu.jpg)


### 糗事百科

![](./images/qiushibaike.gif)

![](./images/qiushibaike.jpg)

## tips of pull request 

- 欢迎大家一起来 pull request 💗

## Problems

- 关于验证码：本项目所用的方法都没有处理验证码，识别复杂验证码的难度就目前来说，还是比较大的。以我的心得来说，做爬虫最好的方式就是尽量规避验证码。
- 代码失效：由于网站策略或者样式改变，导致代码失效，请给我提issue，如果你已经解决，可以提PR，谢谢！
- 正在对部分代码进行优化。。。

## Another
- 如果你有什么比较难登陆的网站，比如发现用了selenium+webdriver都还登陆不了的网站，欢迎给我提issue
- 如果该repo对大家有帮助，给个star鼓励鼓励吧

## something to add

1. 项目写了一段时间后，发现代码的风格和程序的易用性，可扩展性，代码的可读性，都存在一定的问题，所以接下来最重要的是重构代码，让大家可以更容易的做出一些自己的小功能。
2. 如果你觉得某个网站的登录很有代表性，欢迎在 issue 中提出
3. 如果网站的登录很有意思，我会在后面的更新中加入
4. 网站的登录机制有可能经常的变动，所以当现在的模拟的登录的规则不能使用的时候，请在 issue 中提出
5. 如果关注量大的话，我还是会不断维护此仓库带来更多的东西，并且重构代码，
6. 欢迎向我提PR

## Have something to say❗️❗️(Important)
- 今天有人给我说了一些东西，他说：”你今天开源这些东西会让别人容易的反爬虫“。对，我知道，当然我很清楚这些，但是人生总是需要一些挑战不是吗？兄弟？我认为当我攻破他们防守的时刻，才是最刺激的，不是吗？如果没人反抗，我做这些才是真的毫无意义，只有真正的攻与守，才能促使我们进步，时代在变兄弟，科技也在变，安于现状，才是错误的根本原因!
- 希望你们不要安于现状，生活处处是惊喜！

## 🎉Life is fantastic🥳! bro💪~

## Acknowledgments

- Thanks for all 🎉

## 联系我
- My Email : criselyj@163.com
