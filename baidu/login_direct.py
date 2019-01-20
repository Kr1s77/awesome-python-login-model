import time
import json
import re
import requests
import execjs
import rsa
import base64


js_path = 'login.js'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
           }

# 全局的session
session = requests.session()
session.get('https://pan.baidu.com', headers=headers)


def _get_runntime():
    """
    :param path: 加密js的路径,注意js中不要使用中文！估计是pyexecjs处理中文还有一些问题
    :return: 编译后的js环境，不清楚pyexecjs这个库的用法的请在github上查看相关文档
    """
    phantom = execjs.get()  # 这里必须为phantomjs设置环境变量，否则可以写phantomjs的具体路径
    with open(js_path, 'r') as f:
        source = f.read()
    return phantom.compile(source)


def get_gid():
    return _get_runntime().call('getGid')


def get_callback():
    return _get_runntime().call('getCallback')


def _get_curtime():
    return int(time.time()*1000)


# 抓包也不是百分百可靠啊,这里?getapi一定要挨着https://passport.baidu.com/v2/api/写，才会到正确的路由
def get_token(gid, callback):
    cur_time = _get_curtime()
    get_data = {
        'tpl': 'netdisk',
        'subpro': 'netdisk_web',
        'apiver': 'v3',
        'tt': cur_time,
        'class': 'login',
        'gid': gid,
        'logintype': 'basicLogin',
        'callback': callback
    }
    headers.update(dict(Referer='http://pan.baidu.com/', Accept='*/*', Connection='keep-alive', Host='passport.baidu.com'))
    resp = session.get(url='https://passport.baidu.com/v2/api/?getapi', params=get_data, headers=headers)
    if resp.status_code == 200 and callback in resp.text:
        # 如果json字符串中带有单引号，会解析出错，只有统一成双引号才可以正确的解析
        #data = eval(re.search(r'.*?\((.*)\)', resp.text).group(1))
        data = json.loads(re.search(r'.*?\((.*)\)', resp.text).group(1).replace("'", '"'))
        return data.get('data').get('token')
    else:
        print('获取token失败')
        return None


def get_rsa_key(token, gid, callback):
    cur_time = _get_curtime()
    get_data = {
        'token': token,
        'tpl': 'netdisk',
        'subpro': 'netdisk_web',
        'apiver': 'v3',
        'tt': cur_time,
        'gid': gid,
        'callback': callback,
    }
    resp = session.get(url='https://passport.baidu.com/v2/getpublickey', headers=headers, params=get_data)
    if resp.status_code == 200 and callback in resp.text:
        data = json.loads(re.search(r'.*?\((.*)\)', resp.text).group(1).replace("'", '"'))
        return data.get('pubkey'), data.get('key')
    else:
        print('获取rsa key失败')
        return None


def encript_password(password, pubkey):
    pub = rsa.PublicKey.load_pkcs1_openssl_pem(pubkey.encode('utf-8'))
    encript_passwd = rsa.encrypt(password.encode('utf-8'), pub)
    return base64.b64encode(encript_passwd).decode('utf-8')


def login(token, gid, callback, rsakey, username, password):
    post_data = {
        'staticpage': 'http://pan.baidu.com/res/static/thirdparty/pass_v3_jump.html',
        'charset': 'utf-8',
        'token': token,
        'tpl': 'netdisk',
        'subpro': 'netdisk_web',
        'apiver': 'v3',
        'tt': _get_curtime(),
        'codestring': '',
        'safeflg': 0,
        'u': 'http://pan.baidu.com/disk/home',
        'isPhone': '',
        'detect': 1,
        'gid': gid,
        'quick_user': 0,
        'logintype': 'basicLogin',
        'logLoginType': 'pc_loginBasic',
        'idc': '',
        'loginmerge': 'true',
        'foreignusername': '',
        'username': username,
        'password': password,
        'mem_pass': 'on',
        # 返回的key
        'rsakey': rsakey,
        'crypttype': 12,
        'ppui_logintime': 33554,
        'countrycode': '',
        'dv': 'MDEwAAoAEgAKBScAMgAAAF00AA0CABvLy0ru-Kzto-S297rluuq56baC3YLxhOaL4pYJAgAi3d6dnPz8_'
              'Pz8fIWF0ZDemcuKx5jHl8SUy_-g_4z5m_af6wgCACHT0C4u39_fh-66-7XyoOGs86z8r_-glMuU5IX2hfKd7'
              '4sNAgAdy8uYnYXRkN6Zy4rHmMeXxJTL_6D_ivmc7qDBrMkHAgAEy8vLywkCACTT0K-vUFBQUFAC_Pyo6afgs'
              'vO-4b7uve2yhtmG9pfkl-CP_ZkIAgAh09Cvrq6urvyXw4LMi9mY1YrVhdaG2e2y7Z38j_yL5JbyCAIAIdPQe'
              'nqsrKzjo_e2-L_trOG-4bHisu3Zhtms37rIhueK7wwCAB_TNjY2Nn2azo_BhtSV2IfYiNuL1OC_4JXmg_G_3'
              'rPWDAIAH9M2NjY2f287ejRzIWAtci19Ln4hFUoVYBN2BEorRiMMAgAf0zY2NjZ34rb3uf6s7aD_oPCj86yYx5'
              'jtnvuJx6bLrgcCAATLy8vLDAIAH9Pb29vb_CZyM306aClkO2Q0ZzdoXANcKVo_TQNiD2oHAgAEy8vLywwCAB_'
              'TNjY2NhMPWxpUE0EATRJNHU4eQXUqdQBzFmQqSyZDDQIAHcvL6X5mMnM9eihpJHskdCd3KBxDHGkafw1DIk8q'
              'CQIAJNPQUFCOjo6OjqwsLHg5dzBiI24xbj5tPWJWCVYjUDVHCWgFYAgCACHT0KqqWlpaewVREF4ZSwpHGEcXRB'
              'RLfyB_D24dbhl2BGAHAgAEy8vLywkCABTLyPDxOTk5OTkmfH1-fH26uu7u_wgCAAnLyISFCgoKFz4IAgAJy8i'
              'YmR4eHgIoBwIABMvLy8sOAgAByxUCAAjLy8qR4PdMcgECAAbLysrFQbcFAgAEy8vLwQQCAAbAwMLB8MAWAgAi6'
              'p71xevf7dns1ObS6tLr0uPS6tvj0ubf7d_q2-vY6tnu2RcCAA_Lyo6OhNny1YnxwqaBqo0QAgAByxMCABnL3t7'
              'etsK2xvzT_Iztg63Prsej1vib9Jm2BgIAKMvLy4R7hHupqamt6urq6CUlJSCAgICDBwcHAqKioqG8vLy4_____'
              'bwIAgAg3N_n5lhYWEYpWThLOBVlDWIHaQB4VTlQI1d6FnkedxkHAgAEy8vLywwCAB_TNjY2NhAYTA1DBFYXWgVa'
              'ClkJVmI9YhdkAXM9XDFUBwIABMvLy8sIAgAJy8g3N3BwcFwfDQIAHcvL-vXtufi28aPir_Cv_6z8o5fIl-KR9Ib'
              'IqcShDQIAHcvL8ExUAEEPSBpbFkkWRhVFGi5xLlsoTT9xEH0YDAIAH9M2NjY2dq76u_Wy4KHss-y877_g1IvUod'
              'K3xYvqh-IMAgAf0zY2NjZ-cCRlK2w-fzJtMmIxYT4KVQp_DGkbVTRZPAwCAB_TNjY2Nn-azo_BhtSV2IfYiNuL1O'
              'C_4JXmg_G_3rPWDAIAH9M2NjY2fVAERQtMHl8STRJCEUEeKnUqXyxJO3UUeRwIAgAh09BfX7GxseHuuvu18qDhrPO'
              's_K__oJTLlOSF9oXyne-LDQIAHcvLmJSM2JnXkMKDzpHOns2dwvap9obnlOeQ_43pCAIAINzY4uIKCgpdwK7Lv9uyw'
              'ar1heSX5LvXuN-22IfhjvyRDQIAHcvLkGx0IGEvaDp7Nmk2ZjVlOg5RDn4fbB9oB3URDQIAHcvLrOnxpeSq7b_-s'
              '-yz47Dgv4vUi_ua6ZrtgvCUDQIAHcvLS7au-rv1suCh7LPsvO-_4NSL1KTFtsWy3a_L',
        'callback': 'parent.'+callback
    }
    resp = session.post(url='https://passport.baidu.com/v2/api/?login', data=post_data, headers=headers)
    if 'err_no=0' in resp.text:
        print('登录成功')
    else:
        print('登录失败')

if __name__ == '__main__':
    name = input('请输入用户名:\n')
    passwd = input('请输入密码:\n')

    cur_gid = get_gid()
    cur_callback = get_callback()
    cur_token = get_token(cur_gid, cur_callback)
    cur_pubkey, cur_key = get_rsa_key(cur_token, cur_gid, cur_callback)
    encript_pass = encript_password(passwd, cur_pubkey)
    login(cur_token, cur_gid, cur_callback, cur_key, name, encript_pass)

    home_page = session.get('http://pan.baidu.com/disk/home', headers=headers).text
    print(home_page)
