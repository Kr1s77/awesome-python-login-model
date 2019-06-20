# coding:utf-8


from types import FunctionType,LambdaType,CodeType
from functools import wraps
from threading import Thread
from ctypes import c_uint32,c_int32
import math


class Tool(object):
    '''
        准备使用装饰器控制请求的重放，但是还是没想好由外部控制还是内部设定
    '''
    def __init__(self,func):
        wraps(func)(self)
        self.ncalls = 0
    
    def __call__(self,*args,**kw):
        self.ncalls += 1
        return self.__wrapped__(*args,**kw)
    
    def __get__(self,instance,cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self,instance)


class Logs(object):
    pass

class Retry(object):

    def __init__(self,log:bool=False,format:str='',callback:FunctionType=None):
        self.log = log
        self.format = format
        self.callback = callback
    
    def __call__(self,func,*args,**kw):

        @wraps(func)
        def wrapper(obj,**kw):
            res = func(obj,**kw)
            print('Ending')
            res = self.callback(res,obj) if self.callback else res
            return res
        return wrapper

@Retry()
def execute(**kw):
    print(kw)
    return kw

class G:
    @Retry()
    def execute(self,**kw):
        return kw


class BackThread(Thread):

    def __init__(self,func,args:tuple=()):
        super(BackThread,self).__init__()
        self.func = func
        self.args = args
    
    def run(self):
        self.result = self.func(*self.args)
    
    def get_result(self):
        Thread.join(self)
        try:
            return self.result
        except Exception:
            return None


class Encry(object):

    def __init__(self):
        '''淘宝H5登录的一些js加密转成了python'''
        pass

    def encrypt(self,code):
        n = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
        s = ''
        l = 0
        while l < len(code):
            try:
                t = ord(code[l])
            except IndexError as e:
                t = 0# t = math.nan
            l += 1
            try:
                r = ord(code[l])
            except IndexError as e:
                r = 0 # r = math.nan
            l += 1
            try:
                i = ord(code[l])
            except IndexError as e:
                i = 0 # i = math.nan
            l += 1
            o = t >> 2
            a = (3 & t) << 4 | r >> 4
            # if type(r) or type(i) == 'float':
            #     print(r,i)
            u = (15 & r) << 2 | i >> 6
            c = 63 & i
            if r == 0:
                u = c = 64
            else:
                c = 64 if i == 0 else c
            s = s + n[o] + n[a] + n[u] + n[c]
            # print(s)
        return s

    def int_overflow(self,val):
        '''这个函数可以得到32位int溢出结果，因为python的int一旦超过宽度就会自动转为long，永远不会溢出，有的结果却需要溢出的int作为参数继续参与运算'''
        maxint = 2147483647
        if not -maxint-1 <= val <= maxint:
            val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
        return val

    def unsigned_right_shitf(self,n,i):
        # 数字小于0，则转为32位无符号uint
        if n<0:
            n = c_uint32(n).value
        # 正常位移位数是为正数，但是为了兼容js之类的，负数就右移变成左移好了
        if i<0:
            return -self.int_overflow(n << abs(i))
        #print(n)
        return self.int_overflow(n >> i)

    def left_move(self,a,bit):
        return c_int32(a << bit).value

    def ROTL(self,e,t):
        return self.left_move(e,t) | self.unsigned_right_shitf(e,32 - t)

    def toHexStr(self,e):
        n = ''
        for r in range(7,-1,-1):
            t = c_int32(self.unsigned_right_shitf(e,4 * r)).value & c_int32(15).value
            n += hex(t)[2:]
        return n

    def f(self,e,t,n,r):
        '''这里的值计算出来好像没有问题，但是为什么会没有问题？'''
        if e == 0:
            return t & n ^ ~t & r
        elif e == 1:
            return t ^ n ^ r
        elif e == 2:
            return t & n ^ t & r ^ n & r
        elif e == 3:
            return t ^ n ^ r
    
    def hash_encrypt(self,code,status=False):
        if not status:
            code = self.encrypt(code)
        
        r = [1518500249, 1859775393, 2400959708, 3395469782]
        code += chr(128)
        u = len(code) / 4 + 2
        c = math.ceil(u / 16)
        s = [None] * c
        for i in range(c):
            s[i] = [None] * 16
            for a in range(16):
                try:
                    _a = self.left_move(ord(code[64 * i + 4 * a]),24)
                except IndexError:
                    _a = 0
                try:
                    _b = self.left_move(ord(code[64 * i + 4*a + 1]),16)
                except IndexError:
                    _b = 0
                try:
                    _c = self.left_move(ord(code[64 * i + 4 * a + 2]),8)
                except IndexError:
                    _c = 0
                try:
                    _d = ord(code[64 * i + 4 * a + 3])
                except IndexError:
                    _d = 0

                s[i][a] = _a | _b | _c | _d
        s[c - 1][14] = 8 * (len(code) -1) / math.pow(2,32)
        s[c - 1][14] = math.floor(s[c - 1][14])
        s[c - 1][15] = 8 * (len(code) - 1) & 4294967295
        m = 1732584193
        g = 4023233417
        v = 2562383102
        T = 271733878
        S = 3285377520
        C = [None] * 80
        for i in range(c):
            for o in range(16):
                C[o] = s[i][o]
            for o in range(16,80):
                C[o] = self.ROTL(C[o -3] ^ C[o - 8] ^ C[o - 14] ^ C[o - 16],1)
            l = m
            f = g
            d = v
            p = T
            h = S
            for o in range(80):
                y = math.floor(o / 20)
                B = self.ROTL(l,5) + self.f(y,f,d,p) + h + r[y] + C[o] & 4294967295
                h = p
                p = d
                d = self.ROTL(f,30)
                f = l
                l = B
            m = c_int32(m + l).value & c_int32(4294967295).value
            g = c_int32(g + f).value & c_int32(4294967295).value
            v = c_int32(v + d).value & c_int32(4294967295).value
            T = c_int32(T + p).value & c_int32(4294967295).value
            S = c_int32(S + h).value & c_int32(4294967295).value
        
        return self.toHexStr(m) + self.toHexStr(g) + self.toHexStr(v) + self.toHexStr(T) + self.toHexStr(S)
    




if __name__ == '__main__':
    res = G().execute(a=3,b=4,c=5)
    print(res)





