#coding:utf-8

settings = {
    'auto_shutdown':False,  #是否自动关机，默认为False
    'total_products':300,   #要申请的商品个数上限，默认为300
    'total_num_of_page':50, #申请前total_num_of_page页
    'choice':False,      #是否按照商品名称选择要申请的商品，如果设置为True，则应该创建choice.txt文件
                        #并将想要的商品名称写进去即可。默认为False
    'ban':False          #是否按照商品名称选择要过滤掉的商品，如果设置为True，则应该创建ban.txt文件
                        #并将想过滤掉的商品名称写进去即可。(不同商品名称之间用,.!空格或换行符隔开即可)默认为False
}
