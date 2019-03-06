import json

import scrapy
import re
from datetime import datetime
import pandas as pd
import time
from common.util import get_13_time
t = get_13_time()
from liepinSpecialComJob.items import LiepinspecialcomjobItem


class LiepinSpdier(scrapy.Spider):
    name = 'liepin'
    start_urls = ['https://vip.liepin.com/883905/1405577359643.shtml',
                  'https://vip.liepin.com/8161070/joblist.shtml',
                  # 'http://maker.haier.net/custompage/socialchannel/index.html?platformcode=lp',
                  'https://vip.liepin.com/7855333/joblist.shtml',
                  'https://vip.liepin.com/8090130/1409730340536.shtml',
                  'https://vip.liepin.com/8399212/joblist.shtml',
                  'https://vip.liepin.com/1198424/joblist2.shtml',
                  'https://vip.liepin.com/8787971/joblist.shtml',
                  'https://vip.liepin.com/8796178/joblist2.shtml',
                  'https://vip.liepin.com/8091337/1426475303042.shtml',
                  'https://vip.liepin.com/7904788/job.shtml',
                    ]

    def parse(self, response):
        text = response.text
        company_name = re.search(r'<title>(.*?) - 猎聘网招聘官网',text).group(1)
        companyId=re.search(r'CONFIG={"companyId":"([0-9]+)"}',text).group(1)
        next_meta = response.meta
        data = pd.read_csv('G:\workspace\y2019m01\/first_lagou\company300.csv', encoding='gbk')
        try:
            for i in range(len(data)):
                n = 0
                for j in data.loc[i, '股票简称']:
                    if j in company_name:
                        n += 1
                if n == len(data.loc[i, '股票简称']):
                    next_meta['ticker'] = data.loc[i, '股票代码']
                    print(n, next_meta['ticker'], company_name)
        except BaseException as e:
            next_meta['ticker'] ='None'
            print('ticker匹配错误')
        next_meta['company_name'] = company_name
        next_meta['companyId'] = companyId
        url='https://www.liepin.com/ajaxproxy.html'
        # headers={
        #     'Referer':'https://vip.liepin.com/8091337/1426475303042.shtml'
        # }
        yield scrapy.Request(url, callback=self.parse_list, meta=next_meta,dont_filter=True)

    def parse_list(self,response):
        next_meta = response.meta
        companyId = next_meta['companyId'].strip()
        # print(companyId,response.text)
        n=0
        while n<95:
            # try:
            t = get_13_time()
            # 'https://www.liepin.com/company/sojob.json?pageSize=15&curPage=0&ecompIds=8091337&dq=&publishTime=&keywords=&_=1550383073951'
            url=f'https://www.liepin.com/company/sojob.json?pageSize=15&curPage={n}&ecompIds={companyId}&dq=&publishTime=&keywords=&_={t}'
            n+=1
            headers={
                'referer':'https://www.liepin.com/ajaxproxy.html'
            }
            cookies={
                '__uuid': '1550017147980.22',
                '_uuid': 'E4361B46FFA8441973EC46E6488BD983',
                'is_lp_user': 'true',
                'need_bind_tel': 'false',
                'new_user': 'false',
                'c_flag': 'f57e19ed294147b87179e4e6132477f5',
                'imClientId': '45e417dd37f82ac674cdcbb355984626',
                'imId': '45e417dd37f82ac6a36687782a0c1c67',
                'imClientId_0': '45e417dd37f82ac674cdcbb355984626',
                'imId_0': '45e417dd37f82ac6a36687782a0c1c67',
                'gr_user_id': '374534ce-aa54-4880-88ca-7a7bb7adf340',
                'bad1b2d9162fab1f80dde1897f7a2972_gr_last_sent_cs1': '463d81f04fd219c61a667e00ad0d9493',
                'grwng_uid': 'f3fda8f8-0c2e-4f29-8507-f42f7a9671ec',
                'fe_work_exp_add': 'true',
                'ADHOC_MEMBERSHIP_CLIENT_ID1.0': 'fa804ff0-2a02-3f31-8dcb-8e13b527dfcb',
                'bad1b2d9162fab1f80dde1897f7a2972_gr_cs1': '463d81f04fd219c61a667e00ad0d9493',
                '__tlog': '1550383052778.97%7C00000000%7C00000000%7C00000000%7C00000000',
                '_mscid': '00000000',
                'Hm_lvt_a2647413544f5a04f00da7eee0d5e200': '1550233873,1550279247,1550281552,1550383053',
                'abtest': '0',
                '_fecdn_': '0',
                '__session_seq': '2',
                '__uv_seq': '2',
                'Hm_lpvt_a2647413544f5a04f00da7eee0d5e200': '1550383074'
            }
            next_meta['ticker'] = next_meta['ticker']
            print(next_meta['ticker'])
            next_meta['company_name'] = next_meta['company_name']
            print(next_meta['company_name'])
            yield scrapy.Request(url, callback=self.parse_job,meta=next_meta,headers=headers,cookies=cookies)
            # except BaseException as e:
            #     print('已完成最后一页')
            #     break

    def parse_job(self,response):
        meta = response.meta
        item = LiepinspecialcomjobItem()
        text = response.text
        print('****************************************')
        json_data = json.loads(text)
        as_of_date = datetime.now()
        job_infos=json_data['list']
        for job_info in job_infos:
            origin_site=job_info['url']
            job_name=job_info['title']
            salary=job_info['salary']
            city=job_info['city']
            education=job_info['eduLevel']
            work_year=job_info['workYear']
            pub_time=job_info['time']
            function=job_info['dept']

            item['ticker'] = meta['ticker'].strip()
            item['company_name'] = meta['company_name'].strip()
            item['job_name']=job_name
            item['salary']=salary
            item['city']=city
            item['education']=education
            item['work_year']=work_year
            item['pub_time']=pub_time
            item['as_of_date']=as_of_date
            item['function']=function
            item['origin_site']=origin_site

            yield item



        #暂不深挖
        # for url in origin_sites:
        #     yield scrapy.Request(url, callback=self.parse_job)













