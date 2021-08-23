# coding:utf-8

# 目的：作为统一的配置加载，由这个来控制配置文件的更新以及导出
# 第一：文件检查，首先检查有没有配置文件对象，如果没有下载配置文件然后更新文件对象
# 第二：时间判断，请求文件获取到请求的缓存时间然后比对文件的创建时间，如果比创建时间大那么启动更新


import datetime
import pathlib
import os

class FileUpdate(object):

    def __init__(self):
        self.time = datetime.datetime.now()

    def __get__(self,instance,instance_type):
        pass
    
    def __set__(self,instance,value):
        pass



class Config(object):

    def __init__(self):
        self.H5_configURL = ''
        self.Config_manager = {}
    
    def getConfig(self,name):
        return self.Config_manager.get(name,'')



class TSDKError(Exception):

    def __init__(self,errInfo):
        super().__init__(self)
        self.errinfo = errInfo
    
    def __setError(self):
        pass
    
    def __str__(self):
        return self.errinfo
    



if __name__ == '__main__':
    pass