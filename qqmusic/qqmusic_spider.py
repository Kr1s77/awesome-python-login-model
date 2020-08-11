# -*- coding: utf-8 -*-
# @Author: MediocrityXT
# @Github: https://github.com/MediocrityXT


import requests
import execjs
import os

class Spider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Referer':'https://y.qq.com/portal/player.html'
        }
    
    def __get_songs(self, name):
        num = 10        
        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&n='+str(num)+'&w='+name+'&format=json'
        response = requests.get(url, headers=self.headers).json()['data']['song']['list']
        return response

    def __print_info(self, songs):
        #打印搜索到的的歌曲信息
        index = 0
        for it in songs:
            index = index + 1
            if it['pay']['payplay']:
                NeedPay='(收费)  ' 
            else:
                NeedPay='        ' 
            singers=''
            it2=it['singer']
            for x in it2:
                singers = singers+x['name']+' '
            print(index,'.',NeedPay,it['songname'],'     ',singers)

    def __get_Sign(self,data):
        print(os.path.realpath(__file__))
        with open(os.path.realpath(__file__)+'/../sign.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
        js_exec = execjs.compile(js_content)
        sign = js_exec.call('getSecuritySign',data)
        return sign

    def __get_url(self,data):
        sign=self.__get_Sign(data)
        
        url='https://u.y.qq.com/cgi-bin/musics.fcg?-=getplaysongvkey38596056557178904'\
        '&g_tk=1129808082'\
        '&sign={}'\
        '&loginUin=18585073516'\
        '&hostUin=0'\
        '&format=json'\
        '&inCharset=utf8'\
        '&outCharset=utf-8'\
        '&notice=0'\
        '&platform=yqq.json'\
        '&needNewCode=0&data='.format(sign)+data
        response=requests.get(url).json()
        return response['req_0']['data']['midurlinfo'][0]['purl']

    def __set_data(self, songmid):
        data='{"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"358840384","calltype":0,"userip":""}},'\
        '"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"358840384","songmid":["'+songmid+'"],"songtype":[0],"uin":"18585073516","loginflag":1,"platform":"20"}},"comm":{"uin":18585073516,"format":"json","ct":24,"cv":0}}'
        return data

    def __download_mp3(self, url, filename):
        abspath = os.path.abspath('.')  # 获取绝对路径
        os.chdir(abspath)
        response = requests.get(url, headers=self.headers).content
        path = os.path.join(abspath, filename)
        with open(path + '.m4a', 'wb') as f:
            f.write(response)
            print('下载完毕,保存至:%s.m4a' % path )

    def run(self):
        while True:
            name = input('搜索歌曲名称：')
            songs = self.__get_songs(name)
            self.__print_info(songs)
            choice = int(input('请输入左边对应数字选择歌曲:'))-1
            if choice >=0 & choice<len(songs):
                if songs[choice]['pay']['payplay']:
                    print('无法下载收费歌曲')
                else:
                    songmid=songs[choice]['songmid']
                    data=self.__set_data(songmid)
                    url='https://isure.stream.qqmusic.qq.com/'+self.__get_url(data)
                    #print(url)
                    self.__download_mp3(url,songs[choice]['songname'])
            else:
                print('输入错误')
            
            flag = input('如需继续可以按任意键进行搜歌，否则按0结束程序')
            if flag == '0':
                break
        print('程序结束！')
        
if __name__=='__main__':
    spider = Spider()
    spider.run()
