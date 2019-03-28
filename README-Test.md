## Test

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

### 百度翻译
- 输入英语自动翻译

![](./images/baidu_translate.gif)