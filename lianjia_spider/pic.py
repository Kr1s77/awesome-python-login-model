import json
import matplotlib.pyplot as plt
import matplotlib

# 设置中文字体和负号正常显示
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

"""
info:
author:CriseLYJ
github:https://github.com/CriseLYJ/
update_time:2019-3-7
"""


def load_data():
    global data, dic_data
    with open("xm.json", "r", encoding="utf-8") as f:
        str = f.read()
        data = json.loads(str)
    dic_data = dict()
    for i in range(len(data)):
        per_price = (int)(data[i].get("price"))
        region = data[i].get("area")
        # print(per_price,region)
        try:
            dic_data[region].append(per_price)
        except:
            dic_data[region] = [per_price]
    print(dic_data)


def split_data():
    global region_data
    region_data = dict()
    for region in dic_data.keys():
        # 最大值、最小值、平均值
        region_data[region] = {"max": dic_data[region][0], "min": dic_data[region][0], "average": 0}
        for per_price in dic_data[region]:
            if per_price > region_data[region]["max"]:
                region_data[region]["max"] = per_price
            if per_price < region_data[region]["min"]:
                region_data[region]["min"] = per_price
            region_data[region]["average"] += per_price
        region_data[region]["average"] /= len(dic_data[region])
        # 保留两位小数
        region_data[region]["average"] = round(region_data[region]["average"], 2)
    print(region_data)


def data_viewer():
    label_list = region_data.keys()  # 横坐标刻度显示值
    max = []
    min = []
    average = []
    for label in label_list:
        max.append(region_data[label].get("max"))
        min.append(region_data[label].get("min"))
        average.append(region_data[label].get("average"))
    x = range(len(max))
    """
    绘制条形图
    left: 长条形中点横坐标
    height: 长条形高度
    width: 长条形宽度，默认值0
    .8
    label: 为后面设置legend准备
    """
    rects1 = plt.bar(x=x, height=max, width=0.25, alpha=0.8, color='red', label="最大值")
    rects2 = plt.bar(x=[i + 0.25 for i in x], height=average, width=0.25, color='green', label="平均值")
    rects3 = plt.bar(x=[i + 0.5 for i in x], height=min, width=0.25, color='blue', label="最小值")
    # plt.ylim(0, 50) # y轴取值范围
    plt.ylabel("房价/元")
    """
    设置x轴刻度显示值
    参数一：中点坐标
    参数二：显示值
    """
    plt.xticks([index + 0.25 for index in x], label_list)
    plt.xlabel("区")
    plt.title("厦门二手房价格分析图")
    plt.legend()  # 设置题注 # 编辑文本
    for rect in rects1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
    for rect in rects2:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
    for rect in rects3:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
    plt.show()


def main():
    load_data()
    split_data()
    data_viewer()


if __name__ == '__main__':
    main()
