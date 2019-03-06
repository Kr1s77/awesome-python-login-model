import execjs
import requests
import json
import re


def get_session():
    return requests.session()


def get_runntime(path):
    """
    :param path: 加密js的路径,注意js中不要使用中文！估计是pyexecjs处理中文还有一些问题
    :return: 编译后的js环境，不清楚pyexecjs这个库的用法的请在github上查看相关文档
    """
    phantom = execjs.get('PhantomJS')  # 这里必须为phantomjs设置环境变量，否则可以写phantomjs的具体路径
    with open(path, 'r') as f:
        source = f.read()
    return phantom.compile(source)


# 获取经base64编码的用户名
def get_encodename(name, runntime):
    return runntime.call('get_name', name)


# 获取加密后的密码
def get_pass(password, pre_obj, runntime):
    """
    :param password: 登陆密码
    :param pre_obj: 返回的预登陆信息
    :param runntime: 运行时环境
    :return: 加密后的密码
    """
    nonce = pre_obj['nonce']
    pubkey = pre_obj['pubkey']
    servertime = pre_obj['servertime']
    return runntime.call('get_pass', password, nonce, servertime, pubkey)


# 获取预登陆返回的信息
def get_prelogin_info(prelogin_url, session):
    json_pattern = r'.*?\((.*)\)'
    repose_str = session.get(prelogin_url).text
    m = re.match(json_pattern, repose_str)
    return json.loads(m.group(1))


# 使用post提交加密后的所有数据,并且获得下一次需要get请求的地址
def get_redirect(data, post_url, session):
    """
    :param data: 需要提交的数据，可以通过抓包来确定部分不变的
    :param post_url: post地址
    :param session:
    :return: 服务器返回的下一次需要请求的url
    """
    logining_page = session.post(post_url, data=data)
    login_loop = logining_page.content.decode("GBK")
    pa = r'location\.replace\([\'"](.*?)[\'"]\)'
    return re.findall(pa, login_loop)[0]


# 获取成功登陆返回的信息,包括用户id等重要信息
def do_login(session, url):
    return session.get(url).text


if __name__ == '__main__':
    name = input('请输入登录用户名：\n')
    password = input('请输入登录密码：\n')
    session = get_session()
    runntime = get_runntime('./sinalogin.js')
    su = get_encodename(name, runntime)
    post_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&' \
                   'su=' + su + '&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)'

    pre_obj = get_prelogin_info(prelogin_url, session)
    sp = get_pass(password, pre_obj, runntime)

    # 提交的数据可以根据抓包获得
    data = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'useticket': '1',
        'pagerefer': "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
        'vsnf': '1',
        'su': su,
        'service': 'miniblog',
        'servertime': pre_obj['servertime'],
        'nonce': pre_obj['nonce'],
        'pwencode': 'rsa2',
        'rsakv': pre_obj['rsakv'],
        'sp': sp,
        'sr': '1366*768',
        'encoding': 'UTF-8',
        'prelt': '115',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META',
    }

    url = get_redirect(data, post_url, session)
    login_info = do_login(session, url)
    print("你当前使用的是rookiefly实现的微博登陆方式,登陆返回信息为:\n"+login_info)

















