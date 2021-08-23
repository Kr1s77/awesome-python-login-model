# coding:utf-8

import json
import requests
import aiohttp
import aiofiles
import asyncio
# from collections import OrderedDict

class Resovle(object):
    '''解析淘宝api文档'''
    def __init__(self,json_body):
        self.body = json.loads(json_body)
        self.save_func = {}
    
    def getdata(self,body:dict={}):
        data = body or self.body
        if not data.get('success',None):
            return {}
        data = data.get('data',{})
        self.funcname = data.get('apiChineseName','未知应用')
        self.save_func[self.funcname] = {}
        for item in data:           

            # if item == 'apiChineseName':
            #     self.funcname = data[item]
            #     self.save_func[self.funcname] = {}
            if item == 'name':
                self.save_func[self.funcname][item] = data[item]
            
            if item == 'description':
                self.save_func[self.funcname][item] = data[item]
            #不需要公共参数，因为数据对象没有表明自己是否需要授权，无法判断
            # if item == 'publicParams':
            #     #公共参数的添加
            #     if not self.save_func[self.funcname].get('publicParams',None):
            #         self.save_func[self.funcname]['publicParams'] = []
            #     for pubparams in data.get(item,[]):
            #         if pubparams['required']:
            #             self.save_func[self.funcname]['publicParams'][pubparams['name']] = pubparams['required']
            
            if item == 'requestParams':
                #请求参数的添加
                if not self.save_func[self.funcname].get('requestParams',None):
                    self.save_func[self.funcname]['requestParams'] = []
                for params in data.get('requestParams',[]):
                    self.save_func[self.funcname]['requestParams'].append({
                        'name':params['name'],
                        'value':params['demoValue'],
                        "description":params['description'],
                        'required':params['required']
                    })

        return self.save_func

class 淘宝API解析(object):

    def __init__(self):
        self.req = requests.Session()
        # self.cli_session = aiohttp.ClientSession()
        self.head = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        self.cookie = {
            '_tb_token_':'f7bd3bee37ee5'
        }
    
    def getAllapi(self):
        '''获取淘宝所有的API文档，然后再使用异步下载单独命名存储为配置对象文件'''
        res = self.req.get('https://open.taobao.com/handler/document/getApiCatelogConfig.json?scopeId=&treeId=&docId=&docType=&_tb_token_=f7bd3bee37ee5',cookies=self.cookie)
        data = json.loads(res.content)
        if data.get('success',None):
            if data.get('data',{}).get('treeCategories',[]):
                print(data.get('data',{}).get('treeCategories',[])[0]['name'])
                return data.get('data',{}).get('treeCategories',[])[0]['catelogTrees']
        else:
            return data
    
    async def getDetail(self,docId,docType):
        '''使用异步下载api文档'''
        url = f'https://open.taobao.com/handler/document/getDocument.json?treeId=&docId={docId}&docType={docType}&_tb_token_={self.cookie["_tb_token_"]}'
        async with aiohttp.ClientSession(cookies=self.cookie) as cli_session:
            async with cli_session.get(url) as res:
                # with aiofiles.open(file_name,'wb') as f:
                #     f.write(await res.read())
                body = await res.read()
        json_res = Resovle(body.decode('utf-8'))
        return json_res.getdata()
    
    async def main(self):
        ''''''
        res = self.getAllapi();
        if isinstance(res,dict):
            print(res)
            return
        for item in res:
            dt = {}
            name = item.get('name',None) or item.get('treeName',None)
            if name not in ['淘宝客API','淘宝搜索API','会员中心API','淘宝卡券平台','商户API','手淘分享','手机淘宝API']:
                continue
            for doc_item in item.get('catelogList',[]):
                res = await self.getDetail(doc_item.get('docId',285),doc_item.get('docType',2))
                dt.update(res)
            # async with aiofiles.open(name += '.json','wb') as f:
            #     await f.write(json.dumps(dt))
            with open(name + '.json','w') as f:
                # f.write(json.dumps(dt))
                json.dump(dt,f)

    
    


if __name__ == '__main__':
    # with open('./tbk.json',encoding='utf-8') as f:
    #     jstr = f.read()
    # resovle = Resovle(jstr)
    # res = resovle.getdata()
    loop = asyncio.get_event_loop()
    ts = 淘宝API解析()
    loop.run_until_complete(ts.main())
    loop.close()
    # res = ts.getAllapi()
    # for item in res:

    # print(res)
