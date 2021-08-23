# coding:utf-8

from __future__ import absolute_import

try:
    from .SDK基类 import Base
    from ..util.config import TSDKError
except ImportError:
    from SDK基类 import Base

from util.config import TSDKError
from collections import OrderedDict
import time
import json

class TB_openPlatform(Base):
    '''淘宝开放平台的API，用来解析开放平台的配置'''
    
    # def __init__(self,name:'该函数的名称',user_config:'用户配置信息'={},env:"开放平台环境配置"={},req_config:'函数配置信息'={},**kw):
    #     '''接受两个配置，一个是用户配置信息，另一个是函数的参数配置信息'''
    #     super(淘宝开放平台,self).__init__()
    #     #用户参数配置
    #     self.user_config = user_config
    #     #环境参数配置
    #     self.env = env
    #     #请求参数存放，然后需要对参数进行转换
    #     self.req_config = req_config
    #     #请求方式
    #     self.method = 'get' or 'post'
    #     self.publicParams();
    
    def __init__(self,config:dict={
            "appkey":"25263570",
            "appsecret":"36b3bddb45f177575f63511b54c9e655",
            "url":"https://eco.taobao.com/router/rest"
        }):
        '''传入开放平台的配置'''
        super(TB_openPlatform,self).__init__()
        self.config = config
    
    def __init(self):
        self.public_params = OrderedDict()
        if not self.config['appkey'] or not self.config['appsecret']:
            raise TSDKError('缺少appkey或appsecret')
        self.public_params.update({'app_key':self.config['appkey']})
        self.public_params.update({'sign_method':'md5' or 'hmac'})
        self.public_params.update({'timestamp':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())})
        self.public_params.update({'v':'2.0'})
        self.public_params.update({'format':'json'})
    
    def execute(self,apiname:str,datas:dict):
        options = OrderedDict()
        #初始化公共参数
        self.__init()
        datas.update(self.public_params)
        datas.update({'method':apiname})
        if datas.get('sign_method','md5') == 'hmac':
            sign = self.open_Hmacsign(self.config.get('appsecret',None),datas)
        else:
            sign = self.open_Md5sign(self.config.get('appsecret',None),datas)
        datas.update({'sign':sign})

        options.update({'url':self.config['url']})
        options.update({'method':'get'})
        options.update({'params':datas})

        res = self.request(**options)
        return res
    
      



if __name__ == '__main__':

    tb = TB_openPlatform()
    res = tb.execute('taobao.tbk.item.get',{
        'fields':'num_iid,title,pict_url,small_images,reserve_price,zk_final_price,user_type,provcity,item_url,seller_id,volume,nick',
        'q':'女装',
        'cat':'16,18'
    })
    print(res.text)
    
