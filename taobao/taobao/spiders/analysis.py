#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2018-10-06 12:50
# @file : analysis.py
# @software : PyCharm
import numpy as np
from pymongo import MongoClient
from  matplotlib import pyplot as plt
import re,json,jieba,pandas
from collections import Counter
from wordcloud import WordCloud
import seaborn as sns
# matprotlib显示中文
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

# 从mongodb中获取数据
def data_analysis(parameter):
    client = MongoClient('mongodb://admin:zkyr1006@localhost:28018')
    db = client.taobao
    colls = [db.内搭, db.外套, db.牛仔裤, db.秋季套装]
    data=[]
    for coll in colls:
        list_data=coll.aggregate([{'$group': {'_id': 0, parameter: {'$push': '$'+parameter}}}]).next()[parameter]
        data+=list_data
    return data
    # print(provience)

# 商品所属省份分布柱状图
def provience():
    data=[]
    provs=data_analysis('area')
    # print(provience)
    for each in provs:
        prov = (each.split())[0]
        data.append(prov)
    count={}
    for i in data:
        count[i]=data.count(i)
    # print(count)
    prov=list(count.keys())
    nums=list(count.values())
    return prov,nums

def prov_plt():
    prov, nums = provience()
    plt.figure(figsize=(8, 4))
    plt.xticks(rotation=0)
    plt.bar(prov, nums, color='g')
    plt.xlabel('省份')
    plt.ylabel('数量')
    plt.title('不同省份数量分布图')
    plt.legend()
    plt.show()

# 词云及根据词云数据进行分析的柱状图
def cloud_plt():
    def cloud_data():
        title=data_analysis('title')
        titles=[]
        # 对每个标题进行分词
        for each in title:
            title_cut=jieba.lcut(each)
            titles.append(title_cut)

        # 剔除不需要的词语
        title_del=[]
        for line in titles:
            line_del=[]
            for word in line:
                if word not in ['2018','妈妈','❤','】','【',' ','Chinism','工作室','倔强']:
                    line_del.append(word)
            title_del.append(line_del)
        # print(title_del)

        # 元素去重,每个标题中不含重复元素
        title_clean=[]
        for each in title_del:
            line_dist=[]
            for word in each:
                if word not in line_dist:
                    line_dist.append(word)
            title_clean.append(line_dist)

        # 将所有词语转为一个list
        allwords_dist=[]
        for line in title_clean:
            for word in line:
                allwords_dist.append(word)
        # 把列表转为数据框
        allwords_dist=pandas.DataFrame({'allwords':allwords_dist})
        # 对词语进行分类汇总
        word_count=allwords_dist.allwords.value_counts().reset_index()
        # 添加列名
        word_count.columns=['word','count']
        # print(allwords_dist)
        return word_count,title_clean

    def cloud_data_count():
        # 获取商品销量数据
        sell_count = data_analysis('sell_count')
        word_count, title_clean = cloud_data()
        ws_count = []
        # 商品中包含统计的词时，将其销量加入list
        for each in word_count.word:
            i = 0
            s_list = []
            for t in title_clean:
                if each in t:
                    s_list.append(int(sell_count[i]))
                    # print(s_list)
                i += 1
            # 统计一个关键词所包含商品的销量总数
            ws_count.append(sum(s_list))
        # 把列表转为数据框
        ws_count = pandas.DataFrame({'ws_count': ws_count})
        # 把word_count, ws_count合并为一个表
        word_count = pandas.concat([word_count, ws_count], axis=1, ignore_index=True)
        word_count.columns = ['word', 'count', 'ws_count']
        # 升序排列
        word_count.sort_values('ws_count', inplace=True, ascending=True)
        # 取最大30行数据
        df_ws = word_count.tail(30)
        return df_ws

    # 图云部分
    word_count=cloud_data()[0]
    # 设置字体，背景颜色，字体最大号，
    w_c=WordCloud(font_path='/usr/local/lib/python3.6/dist-packages/matplotlib/mpl-data/fonts/ttf/simhei.ttf',
                  background_color='white',
                  max_font_size=60,
                  margin=1)
    # 取前400个词进行可视化
    wc=w_c.fit_words({x[0]:x[1] for x in word_count.head(1000).values})
    # 设置图优化
    plt.imshow(wc,interpolation='bilinear')
    # 去除边框
    plt.axis('off')
    plt.show()

    # 统计分析柱状图部分
    data = cloud_data_count()
    index = np.arange(data.word.size)
    # plt.figure(figsize=(6,12))
    plt.barh(index, data.ws_count, align='center', alpha=0.8)
    plt.yticks(index, data.word)
    # 添加数据标签
    for y, x in zip(index, data.ws_count):
        plt.text(x, y, '%.0f' % x, ha='left', va='center')
    plt.show()


def impact_analysis():
    sell_count=pandas.DataFrame({'sell_count': data_analysis('sell_count')})
    price=[]
    for i in data_analysis('price'):
        p=i.split('-')
        p_i=p[0].split('.')
        price.append(p_i[0])
    price=pandas.DataFrame({'price':price})
    infos=pandas.concat([sell_count, price], axis=1, ignore_index=True)
    infos.columns = ['sell_count', 'price'] #一定注意定义到columns
    infos['sell_count']=infos.sell_count.astype('int')
    infos['price']=infos.sell_count.astype('int')
    infos['GMV']=infos['sell_count']*infos['price']
    # print(infos.GMV.dtype)
    sns.regplot(x='price',y='GMV',data=infos)
    # sns.lmplot(x='price',y='GMV',data=infos,x_jitter=.05)
    plt.show()

def mean_sale():
    prov,nums=provience()
    sell_count = data_analysis('sell_count')
    areas=[]
    count=[]
    for i in data_analysis('area'):
        areas.append((i.split(' '))[0])
    for each in prov:
        counts=[]
        for i in range(0,len(areas)):
            if each==areas[i]:
                counts.append(int(sell_count[i]))
        count.append(sum(counts))
    # print(count)
    count=pandas.DataFrame({'count':count})
    prov=pandas.DataFrame({'prov':prov})
    nums=pandas.DataFrame({'nums':nums})
    data = pandas.concat([nums,count], axis=1, ignore_index=True)
    data.columns = ['nums','count']
    data['nums']=data.nums.astype('int')
    m_l=data['count']/data['nums']
    mean_list=[]
    for each in m_l:
        each=str(each).split('.')
        mean_list.append(each[0])
    mean_list=pandas.DataFrame({'mean_list':mean_list},dtype=np.int)
    infos = pandas.concat([prov,mean_list], axis=1, ignore_index=True)
    infos.columns = ['prov','mean_list']
    infos['mean_list']=infos.mean_list.astype('int')
    infos.sort_values('mean_list',inplace=True,ascending=False)
    infos=infos.reset_index()
    index=np.arange(infos.mean_list.size)
    print(infos)
    plt.figure(figsize=(8,4))
    plt.bar(index,infos.mean_list,color='purple')
    plt.xticks(index,infos.prov,rotation=0)
    plt.xlabel('省份')
    plt.ylabel('平均销量')
    plt.title('不同省份销量分布')
    plt.show()

mean_sale()

# def hot_map():

