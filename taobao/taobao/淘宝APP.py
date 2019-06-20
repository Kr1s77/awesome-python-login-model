# coding:utf-8

from __future__ import absolute_import


try:
    from .SDK基类 import Base
except ImportError:
    from SDK基类 import Base
from collections import OrderedDict

class TB_APP(Base):

    def __init__(self,config:dict={
        "domain":"https://acs.m.taobao.com"
        }):
        '''淘宝app类暂时不做更改，因为暂时也是无用'''
        self.config = config
        self.appConfig = {
            'trip':''
        }
        super(TB_APP,self).__init__()
    
    def getAppkey(self,Appname:str):
        return self.appConfig.get(Appname,'21646297')
    
    def execute(self,datas:dict):
        pass
    


if __name__ == "__main__":
    ts = TB_APP()