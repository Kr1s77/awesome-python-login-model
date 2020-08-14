# -*- coding: utf-8 -*-
# @Author: CriseLYJ
# @Date:   2020-08-14 13:48:23

import requests
import math
import random
from Crypto.Cipher import AES
import base64
import codecs
import os


class decrypt_music(object):
    def __init__(self, d):
        self.d = d
        self.e = '010001'
        self.f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5a" \
                 "a76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46be" \
                 "e255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.g = '0CoJUm6Qyw8W8jud'
        self.random_text = self.get_random_str()

    def get_random_str(self):
        str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        res = ''
        for x in range(16):
            index = math.floor(random.random() * len(str))
            res += str[index]
        return res

    def aes_encrypt(self, text, key):
        iv = b'0102030405060708'
        pad = 16 - len(text.encode()) % 16
        text = text + pad * chr(pad)
        # fix: https://github.com/Kr1s77/awesome-python-login-model/issues/100#issuecomment-673897848
        # error: TypeError: Object type <class 'str'> cannot be passed to C code
        encryptor = AES.new(key.encode(), AES.MODE_CBC, iv)
        msg = base64.b64encode(encryptor.encrypt(text.encode()))
        return msg

    def rsa_encrypt(self, value, text, modulus):
        '''进行rsa加密'''
        text = text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(value, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def get_data(self):
        params = self.aes_encrypt(self.d, self.g)
        params = self.aes_encrypt(params.decode('utf-8'), self.random_text)
        enc_sec_key = self.rsa_encrypt(self.e, self.random_text, self.f)
        return {
            'params': params,
            'encSecKey': enc_sec_key
        }


class Spider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Cookie': '_iuqxldmzr_=32; _ntes_nnid=8d4ef0883a3bcc9d3a2889b0bf36766a,1533782432391; _ntes_nuid=8d4ef0883a3bcc9d3a2889b0bf36766a; __utmc=94650624; WM_TID=GzmBlbRkRGQXeQiYuDVCfoEatU6VSsKC; playerid=19729878; __utma=94650624.1180067615.1533782433.1533816989.1533822858.9; __utmz=94650624.1533822858.9.7.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; WM_NI=S5gViyNVs14K%2BZoVerGK69gLlmtnH5NqzyHcCUY%2BiWm2ZaHATeI1gfsEnK%2BQ1jyP%2FROzbzDV0AyJHR4YQfBetXSRipyrYCFn%2BNdA%2FA8Mv80riS3cuMVJi%2BAFgCpXTiHBNHE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee84b674afedfbd3cd7d98b8e1d0f554f888a4abc76990b184badc4f89e7af8ece2af0fea7c3b92a91eba9b7ec738e8abdd2b741e986a1b7e87a8595fadae648b0b3bc8fcb3f8eafb69acb69818b97ccec5dafee9682cb4b98bb87d2e66eb19ba2acaa5bf3b6b7b1ae5a8da6ae9bc75ef49fb7abcb5af8879f87c16fb8889db3ec7cbbae97a4c566e992aca2ae4bfc93bad9b37aab8dfd84f8479696a7ccc44ea59dc0b9d7638c9e82a9c837e2a3; JSESSIONID-WYYY=sHwCKYJYxz6ODfURChA471BMF%5CSVf3%5CTc8Qcy9h9Whj6CfMxw4YWTMV7CIx5g6rqW8OBv04YGHwwq%2B%5CD1N61qknTP%2Fym%2BHJZ1ylSH1EabbQASc9ywIT8YvOr%2FpMgvmm1cbr2%2Bd6ssMYXuTlpOIrKqp%5C%2FM611EhmfAfU47%5CSQWAs%2BYzgY%3A1533828139236'

        }

    def __get_songs(self, name):
        d = '{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","s":"%s","type":"1","offset":"0","total":"true","limit":"30","csrf_token":""}' % name
        wyy = decrypt_music(d)
        data = wyy.get_data()
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        response = requests.post(url, data=data, headers=self.headers).json()
        return response['result']

    def __get_mp3(self, id):
        d = '{"ids":"[%s]","br":320000,"csrf_token":""}' % id
        wyy = decrypt_music(d)
        data = wyy.get_data()
        url = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token='
        response = requests.post(url, data=data, headers=self.headers).json()
        print(response)
        return response['data'][0]['url']

    def __download_mp3(self, url, filename):
        abspath = os.path.abspath('.')
        os.chdir(abspath)
        response = requests.get(url, headers=self.headers).content
        path = os.path.join(abspath, filename)
        with open(filename + '.mp3', 'wb') as f:
            f.write(response)
            print('下载完毕,可以在%s   路径下查看' % path + '.mp3')

    def __print_info(self, songs):
        """打印歌曲需要下载的歌曲信息"""
        songs_list = []
        for num, song in enumerate(songs):
            print(num, '歌曲名字：', song['name'], '作者：', song['ar'][0]['name'])
            songs_list.append((song['name'], song['id']))
        return songs_list

    def run(self):
        while True:
            name = input('请输入你需要下载的歌曲：')
            songs = self.__get_songs(name)
            if songs['songCount'] == 0:
                print('没有搜到此歌曲，请换个关键字')
            else:
                songs = self.__print_info(songs['songs'])
                num = input('请输入需要下载的歌曲，输入左边对应数字即可')
                url = self.__get_mp3(songs[int(num)][1])
                if not url:
                    print('歌曲需要收费，下载失败')
                else:
                    filename = songs[int(num)][0]
                    self.__download_mp3(url, filename)
                flag = input('如需继续可以按任意键进行搜歌，否则按0结束程序')
                if flag == '0':
                    break
        print('程序结束！')


if __name__ == '__main__':
    spider = Spider()
    spider.run()
