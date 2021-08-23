# coding:utf-8

from __future__ import absolute_import

try:
    from .SDK基类 import Base
except ImportError:
    from SDK基类 import Base



class Alipay_openPlatform(Base):

    def __init__(self):
        super(Alipay_openPlatform,self).__init__()
    
    def execute(self,apiname):
        pass



if __name__ == '__main__':
    pass