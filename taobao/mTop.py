# coding:utf-8
try:
    from .taobao.淘宝H5 import TB_H5
    from .taobao.淘宝开放平台 import TB_openPlatform
    from .taobao.SDK基类 import Base
    from .util.tools import BackThread,Encry
except ImportError as e:
    from taobao.淘宝H5 import TB_H5
    from taobao.淘宝开放平台 import TB_openPlatform
    from taobao.SDK基类 import Base

    from util.tools import BackThread,Encry

import json
# from threading import Thread
from time import sleep,strftime,time
from requests.cookies import RequestsCookieJar
from urllib.parse import urljoin,parse_qsl,urlparse,quote
from collections import OrderedDict
import re
from random import random

class Client(Base):

    def __init__(self):
        super(Client,self).__init__()
        self.H5 = TB_H5()
        self.open = TB_openPlatform()
        self.encry = Encry()
        self.setcookie()
    
    # def __first(self,domain:str='https://h5api.m.taobao.com',url:str="/h5/mtop.taobao.wireless.home.load/1.0/?appKey=12574478"):
    #     '''
    #         必须首先请求一个api来获取到h5token
    #         有多个API时，需要先获取多个API下面的token
    #         如果是https://h5api.m.tmall.com下的API也是需要先获取token的
    #     '''
    #     res = self.get(urljoin(domain,url))
    #     return res

    def setcookie(self):
        _uab_collina = ''
        for i in range(20):
            if len(_uab_collina) < 11:
                _uab_collina += str(random())[2:]
            else:
                break
        #第一个cookie,domain为login.taobao.com，path为/member
        _uab_collina = str(int(time() * 1000)) + _uab_collina[len(_uab_collina) - 11:]
        self.H5.cookies.set('_uab_collina',_uab_collina,domain='login.taobao.com',path='/member')

        #第二个cookie，请求这个JS，https://log.mmstat.com/eg.js，然后把etag的值设置为cna
        res = self.H5.get('https://log.mmstat.com/eg.js')
        cna = re.findall(r'Etag="(.*?)"',res.text)[0]
        self.cookies.set('cna',cna,domain='.taobao.com',path='/')

        #第三个cookie，isg为算法生成的，不好破解，domain为.taobao.com，path为/
        isg = 'BM3NGuFcrQh-tgkk_KLDk9jr3OlHqgF8pnooOQ9SCWTTBu241_oRTBuUcNrFxhk0'
        self.H5.cookies.set('isg',isg,domain='.taobao.com',path='/')

        #第四个cookie，l为算法生成,domain为.taobao.com，path为/
        l = 'bBgKwFjlv-QtIl3JBOCanurza77OSIRYYuPzaNbMi_5pK6T_Bk7OlgnjDF96Vj5RsxYB4-L8Y1J9-etkZ'
        self.H5.cookies.set('l',l,domain='.taobao.com',path='/')  
    
    def login(self,umid_token,domain:str='https://www.taobao.com'):
        self.defaulturl = domain
        # self.H5.get(f'https://login.taobao.com/member/login.jhtml?redirectURL={domain}')
        self.H5.get(f'https://login.taobao.com/member/login.jhtml?allp=&wbp=&sub=false&sr=false&c_is_scure=&from=tbTop&type=1&style=&minipara=&css_style=&tpl_redirect_url={quote(domain)}&popid=&callback=&is_ignore=&trust_alipay=&full_redirect=&need_sign=&sign=&timestamp=&from_encoding=&qrLogin=&keyLogin=&newMini2=')
        res = self.H5.get(f'https://qrlogin.taobao.com/qrcodelogin/generateQRCode4Login.do?adUrl=&adImage=&adText=&viewFd4PC=&viewFd4Mobile=&from=tb&appkey=00000000&umid_token={umid_token}')
        # data = json.loads(res.text)
        # thd = self.checkState(data['lgToken'],umid_token,timeout)
        return res
    
    def checkState(self,lgToken,umid_token,timeout):
        '''在闭包中修改变量要使用nonlocal关键字'''
        def run():
            nonlocal timeout
            # locals()['lgToken'] = lgToken
            # locals()['umid_token'] = umid_token
            # locals()['timeout'] = timeout
            # print(lgToken)
            while timeout > 0:
                self.H5.headers.update({
                            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                            'Referer':'https://login.taobao.com/member/login_unusual.htm?user_num_id=2979250577&is_ignore=&from=tbTop&style=&popid=&callback=&minipara=&css_style=&is_scure=true&c_is_secure=&tpl_redirect_url=https%3A%2F%2Fwww.taobao.com%2F&cr=https%3A%2F%2Fwww.taobao.com%2F&trust_alipay=&full_redirect=&need_sign=&not_duplite_str=&from_encoding=&sign=&timestamp=&sr=false&guf=&sub=false&wbp=&wfl=null&allp=&loginsite=0&login_type=11&lang=zh_CN&appkey=00000000&param=7nmIF0VTf6m%2Bbx8wuCmPLTEdh1Ftef8%2B5yUA%2FXNtAI%2FfMwadkeaCast40u2Ng0%2FC7Z75sOSVLMugWTqKjJ7aA55JYIL%2FPDFJ7zaJhq9XSVUOX%2B1AxQatuIvw4TXGJm1VG4alZ2UohVAAt5WTLYbs5im077nTG%2BOkovORQNtMCEzWKMe0xcuienFAhsBhC0V7qIYZJvPGOOEt0tORA8Fv1zYPuOkWEPDFsPwYG5xj4LTKNZt5HSRRHkviiPy9AJ9uC%2Bs7V%2FQ7b6K07YUG1fA3tFwALGnorSUXRdhcXUBBAt6IiyStIkWFWDgJEymOAXOS5RNGlO1EL5ppmpQas7BarrW2Krui4bxV81AJXyxLfnk3MOxI2dUNdO9VQNY0F6a6nk%2FCzUfR0NfPRrIoXuZDn2N01A8q5XGrMlWmBCH5%2FSKz6%2F%2BrUx3%2FxQTYWmgV49rVSdtySIHip5PsrXHWXCbHqscdve540l5CUKTT7znsoL45pth%2FosxMUb649Yw1EPAq'
                        })
                res = self.H5.get(f'https://qrlogin.taobao.com/qrcodelogin/qrcodeLoginCheck.do?lgToken={lgToken}&defaulturl={self.defaulturl if hasattr(self,"defaulturl") else "www.taobao.com"}')
                data = json.loads(res.text)
                if data['code'] == '10006':
                    print(data)
                    url = data['url'] + '&umid_token=' + umid_token
                    res_main = self.H5.get(url)
                    print('扫码成功')
                    if res_main.url.find('login_unusual.htm') > -1:
                        print('需要安全验证登录')
                        return False
                        # URL = re.findall(r"url:'(.*?)',",res_main.text)[0] if re.findall(r"url:'(.*?)',",res_main.text) else None
                        # if not URL:
                        #     status = False
                        # res = self.H5.get(URL)
                        # txt = res.text.replace(re.findall(r'''"tipsInfo":".*?",''',res.text)[0],'')
                        # data = json.loads(re.findall(r"value='(.*?)'",txt)[0])
                        # param = data.get('param')
                        # target = data.get('options')[0]['optionText'][0]['code']
                        # self.H5.headers.update({'Origin':'https://aq.taobao.com','Referer':'https://aq.taobao.com/durex/validate?param=7nmIF0VTf6m%2Bbx8wuCmPLV6h%2FBQmDRI8eV0OZyuo1fwa%2FgvJ5VoYvhtsoSv%2BF6cVUYizmLOxpLs2mfNAJ8vsGbcBnf0mzB1xSKqsSGvUqY%2Bq5%2FxX1gBcxe0gF0LFtAmr%2FWJFjntGTKMrtyIKbwf5ouytcdZcJseqVq8v%2Fy9%2FeTX4wWc9LeLhPtz8D7l%2FxF%2BCIJggV7kbXlu7mGPRB7pECo%2B2ziHSK%2BByv5YxyYP2zNhUh4QXk5GvHVwJW%2Bua9aMJPAoVN5qoDgqHkrh2z5WYxiZzWy%2BtzWY2652vDwnjI%2F1O7f%2BQy7nknGS71GKCQqOGs3AMkiRA4F2Fhe5TrpbLcH6HfmPw4xL2Y%2BTM1%2F6RVEHcLNdcER2hJ89lHMKhuywTXjzIEiEJAa7NzBo6GJAS2iAUs1CRfB5KaLZHD%2FA1QCQQXiS%2F8FgFVV%2FnCMMCninEOgC%2FLnlUcHBCWBb8kdeKUOAQKft0cdJbKwTKZRdNvxGePGPRtvDX%2Bk7xAUDsqTuPoR6d2gik3XA8G1nKKH%2BEZ8lneUmpZXuM0t1kVDQM4qYfrTw3yLxh6g%3D%3D&redirecturl=https%3A%2F%2Flogin.taobao.com%2Fmember%2Flogin_mid.htm','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})
                        # res = self.sendcode(param,target)
                        # code = ''
                        # res = self.checkcode(param,code,target)
                        # urls = re.findall(r'"(.*?login_by_safe.htm.*?)"',res_main.text)
                        # print(urls)
                        # res = self.H5.get(urls[1])
                        # dt = OrderedDict(parse_qsl(URL.query))
                        
                        # res2 = self.H5.get(f'https://aq.taobao.com/durex/validate?param={dt["param"]}&redirecturl=https%3A%2F%2Flogin.taobao.com%2Fmember%2Flogin_mid.htm')
                        # print(res2.url)
                        
                    return True
                    break
                elif data['code'] == '10001':
                    print('正在扫码')
                    sleep(1)
                    continue
                elif data['code'] == '10004':
                    timeout = 0
                    break
                elif data['code'] == '10000':
                    # print(data['message'])
                    pass
                timeout -= 1
                sleep(1)
            return False
        
        # thd = Thread(target=run)
        thd = BackThread(run,())
        return thd

    def sendcode(self,param:str='',target=''):
        domain = 'https://aq.taobao.com/durex/sendcode'
        data = {
            'checkType':'phone',
            'target':target,
            'safePhoneNum':'',
            'checkCode':''
        }
        res = self.H5.post(domain,params={'param':param,'checkType':'phone'},data=data)
        
        try:
            data = json.loads(res.text)
            print(data.get('message') or '发送失败')
        except Exception as e:
            print(res.text)
        return res
    
    def checkcode(self,param,code,target):
        '''淘宝安全登录验证'''
        head = {'origin':'https://aq.taobao.com'}
        domain = 'https://aq.taobao.com/durex/sendcode'
        data = {
            'checkType':'phone',
            'target':'',
            'safePhoneNum':'',
            'checkCode':code,
            'pageLog':{
                'actions':[
                    {'result':'true','target':'其他验证方式','targetType':'a','attr':'','userTime':strftime('%Y-%m-%d %H:%M:%S'),'type':'operation'},
                    {'result':'true','target':'手机短信验证','targetType':'div','attr':'','userTime':strftime('%Y-%m-%d %H:%M:%S'),'type':'operation'},
                    {'result':'true','target':'确定','targetType':'button','attr':'','userTime':strftime('%Y-%m-%d %H:%M:%S'),'type':'operation'}
                ]
            }
        }
        res = self.H5.post(domain,params={'param':param},data=data)
        try:
            data = json.loads(res.text)
            print(data.get('message') or '发送失败')
        except Exception as e:
            print(res.text)
        return res

    def sendMsg(self,phone,url:str='https://login.m.taobao.com/sendMsg.do'):
        self.H5.get('https://login.m.taobao.com/msg_login.htm?spm=0.0.0.0&ttid=h5%40iframe&redirectURL=https%3A%2F%2Fh5.m.taobao.com%2Fother%2Floginend.html%3Forigin%3Dhttps%253A%252F%252Fmain.m.taobao.com')
        um_token = self.um_token if hasattr(self,'um_token') else self.get_umtoken()
        form = {
            'TPL_username':phone,
            'ncoSig':'',
            'ncoSessionid':'',
            'ncoToken':'',
            'um_token':um_token,
            'ua':'115#1UEIUf1O1TNL1lTDtfGe1CsoE51MI9A11g2u1N2ZKC11q8VlGODHhBlfyzFiNIfyMx/8y5cWi/JJhUUzsoOck86fuzEpOSAyet/8s6IpNbn4eUU4AkN2aYBXuW1QGVysFKT4y5oQiQJJhzU4AWND5YpXyrPQASv4eK/8uSPpgQJRhKAbwzmFZL1010F9dPYMTT9cxCNRlGgmOxpbEFkRe8qIfoxy7pl1yFwqawuBxnihuX5JPN5sYlslAvHUQDZegJuNJ3ED+pTSNDNeHR8PwP/4CjnjTGSLpKqJr63y5qX6Qr8L+kMQ/6Q+27fNulWSpMnOl389bwum8I66eZCn5ICKxvk2hhVzRo6Jbj3vN01kYgauHzEStRXEyjMygV8G06FpIWqJ7EwSO9u1npAOv3MXhII5hTcio6YVz92pF6vCMHvxbsL3ISLy/yUnHM9HiQhyc1ffofR6uNd3TQCFAffrknFNmIMjkqTV/b3sBxns9cMWfUsnR9ueur1SEBL5ZdNYl/tnFU33wwmffwGk4bl5DAx3/HpDH88R356aSLJmi8hfb4OvWsMhp2DAmf6O4sZewL6noDmMfCdW3vyLHd2lPAiDUwRHisnPRSsgUIyRDS+F7M8Z4IxmYrmZg269gzRIaUcJkglgoNQ7AvHqP+qpLUsgo6MUE1/8FrIanONOaEG='
        }
        res = self.H5.post(url,form)
        print(res.text)
        data = json.loads(res.text)
        return data

    
    def msgForm(self,phone:str,sms_code:str,options:dict={}):
        url = 'https://login.m.taobao.com/msg_login.htm'
        
        form = {
            'TPL_username':phone,
            'msgCheckCode':sms_code,
            'otherLoginUrl':'https://login.m.taobao.com/login.htm?nv=true&spm=0.0.0.0&ttid=h5%40iframe&redirectURL=https%3A%2F%2Fh5.m.taobao.com',
            'action':'MsgLoginAction',
            'event_submit_do_login':1,
            'ncoSig':'',
            'ncoSessionid':'',
            'ncoToken':'',
            'TPL_redirect_url':'https://h5.m.taobao.com',
            'loginFrom':'WAP_TAOABO',
            'smsTime':'',
            'smsToken':'',
            'page':'msgLoginV3',
            'um_token':self.um_token if hasattr(self,'um_token') else self.get_umtoken(),
            'ua':'115#1bF1c11O1TZ9MHu5tfGe1CsoE51MI9A11g2u1N2ZKC11q8VlGODHXfOYPaFGsbtzDLoa0/Xn8SNPe/a8yWdi9n4VnJrVt9m5w8pXyrrQ9yffe3VGyWTzG/rkh4zNAWIDZTnwyzy7ASVyeKQ4uWNQi/W5hX/1x11yaTBfy5fpOSAyFKThTyipiQJJv4U4OkN2aTBfurPIASAPetT8u7SQi/WRKB1COWND/BNDHDKpvd1OL+MQSFAFFKjH17QffqcK8w4z0jzTU6N6JM4+4puJ2M+Ph4lZPOuTMTKkxfT8qIYQdi1PDPZaH0EarDs8wF+6RCixRgqIpvyZAkR4LV7p2yEzWVDkPy/zS0LSIrHvYPbDo0Wcp2iZd1l6p04vjBwtD0D5Jx/qQkzIwQhR0Qi+CM1Y1BWgaSF9ipXhirSznvmx68tlGAIBgX1IL9b21Sr3YOTdVVOoP/JE+6TG9ugUXCNWATtXJ0yYxIfWbyriL7f4gGfuugKcPMa1WqT0/4B1DG/Y85suJRPGQZ5qRIDqJG5IDDiXvtnttb6Z0ON0VR8Jj8+J6pLUzmbzYa6n62AxdcNADWJHpbXWR+ZmEZqMLjy2Z1xrcnwZ1voco68WYsWh2sMg2dWzSlNLQP9fMWQ/mGUmRg8k2LQEpD4abJLUj8AlPwnIOY76iuNt+ZhJLvbrEJX4GTIy+xzN1XG1W6GO6gIwxLpi8BWrGG5gagbjRfJPX40tdZgyaOREdQzmS7eSDVky8SL+V54qHEIYWYjYWVjj'
        }

        if options:
            form.update(options)
        
        res = self.H5.post(url,data=form,params={'spm':'','ttid':'h5@iframe','redirectURL':'https://h5.m.taobao.com/other/loginend.html?origin=https%3A%2F%2Fmain.m.taobao.com'})
        # print(res.text)
        return res

    def getUid(self,url:str='https://ynuf.alipay.com/uid'):
        '''获取的缓存id'''
        res = self.H5.get(url)
        print(res.text)
        try:
            cid = res.text[11:-3]
        except Exception:
            cid = ''
        return cid

    def get_umtoken(self,url='https://ynuf.aliapp.org/service/um.json'):
        '''获取um_token'''
        #获取cna的cookie值
        res = self.H5.get('https://log.mmstat.com/eg.js',timeout=3000)
        res = self.H5.post(url,data={'data':'106!h5xmc0clzUWcx81sHmHI4lxmYX+lQzGzUUam0LHtKjRU56cmfapq6YcPzdHCncxrQGoudp7HxfbvZ28EKYD9SajrWgZPvQJHaDBqufIBJ8Gmo9RvclZwCI2Jm7Gef18rbdkP3jz7HrVjMfzEZCh1URFsPTXJOFYU4v/SP7Eg1UkkyTAZPlZ1U4FJw7v/iu/IKVCU5u8Es+ZU52aU6qOw/RuAPJX2Y77K5FaU4ujcNp+paodlQqjiFQRpLlbR64f5lZqlaS5LVNVllBllQFwurplyr4PhiWaQ4WLU5UWcTtebPSc1+VQOGrk/lJ5DSxgYiC6+WyB6mb47wVVktIKkdQI29yQSLsiR363Bo+90mJc0lpX93brWWL6AUItxxVAUnU+QiddYaSBHsP2diFw267UCSs+h6aoDns7QNR+RgZFcWqLZ7kFMNFy4OPPMvMmHvRsoJUPRzmbFVVHR3em9ie8N7DX6Wk9aNC/mA0GcDuEhxIuT9P1yXADX639yLvkiZ7aFkVU4iaQpOAD+N5on2JHSogWDyjO4fwHARigFGVBxwSPafUYu50nLvB9MlI8yy5RnhoArL/X1fIC4Mp2pOx+Vyml8oKlKcNwoArxzNwT7uFyEklLulzt1wXE=','xa':'taobao_mlogin','xt':''})
        psdata = json.loads(res.text)
        um_token = psdata.get('tn')
        self.um_token = um_token
        data = {
            'etf':'',
            'xa':'',
            'siteId':'',
            'uid':'',
            'eml':'AA',
            'etid':'',
            'esid':'',
            'bsh':398,
            'bsw':360,
            'cacheid':self.getUid(),
            'eca':self.H5.cookies.get('cna',''),
            'ecn':"0853e2dc2b17946f6cf315e412fb6b40a4aa9ec7",
            'eloc':'https%3A%2F%2Flogin.m.taobao.com%2Fmsg_login.htm',
            'ep':self.encry.hash_encrypt(''),
            'epl':0,
            'epls':'',
            'esid':'',
            'esl':False,
            'est':2,
            'etf':'b',
            'etid':'',
            'ett':int(time() * 1000),
            'etz':480,
            'ips':'',
            'ms':'445388',
            'nacn':'Mozilla',
            'nan':'Netscape',
            'nce':True,
            'nlg':'zh-CN',
            'plat':'Win32',
            'sah':640,
            'saw':360,
            'sh':640,
            'sw':360,
            'type':'pc',
            'uid':'',
            'xs':'',
            'xt':self.getUmidToken(),
            'xv':'3.3.7'
        }
        res = self.H5.post(url,data={'data':'ENCODE~~V01~~' + self.encry.encrypt(json.dumps(data,separators=(',',':')))})
        print(res.text)
        _id = json.loads(res.text)
        self.H5.cookies.set('_umdata',_id.get('id'),domain='login.m.taobao.com',path='/')
        return um_token

if __name__ == '__main__':
    
    top = Client()
    # umid_token = top.getUmidToken()
    # res = top.login(umid_token)
    # print(res.text)
    # # cookie = {
    # #     '.login.taobao.com':top.cookies.get_dict('.login.taobao.com'),
    # #     '.taobao.com':top.cookies.get_dict('.taobao.com')
    # # }
    # # jar = RequestsCookieJar()
    # # for domain in cookie:
    # #     for name in cookie[domain]:
    # #         jar.set(name,cookie[domain][name],path='/',domain=domain)
    # # top.H5.cookies.update(jar)
    # data = json.loads(res.text)
    # thr = top.checkState(data['lgToken'],umid_token,120)
    # thr.start()
    # res = thr.get_result()
    # print(res)
    # top.H5.headers = {
    #     'Referer':'https://s.m.taobao.com/h5?event_submit_do_new_search_auction=1&_input_charset=utf-8&topSearch=1&atype=b&searchfrom=1&action=home%3Aredirect_app_action&from=1&sst=1&n=20&buying=buyitnow&q=%E7%94%B7%E8%A3%85',
    #     'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 7.0; MI 4S MIUI/8.9.13)'
    # }
    phone = input('请输入手机号：')
    smsdata = top.sendMsg(phone)
    if smsdata.get('success'):

        smscode = input('请输入验证码：')
        res = top.msgForm(phone,smscode,{'smsTime':smsdata.get('smsTime'),'smsToken':smsdata.get('smsToken')})
        # print(res.text)
    else:
        print(smsdata.get('message'))
    
    res = top.H5.execute({
        'api':'mtop.taobao.shop.impression.intro.get',
        'v':'1.0',
        'type':'originaljson',
        'AntiCreep':'true',
        'dataType':'json',
        'data':{'sellerId':17112733,'shopId':61044576}
    })
    print(res)
