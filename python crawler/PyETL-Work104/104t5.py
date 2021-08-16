import requests
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import chardet
import random


# get title company there's link
def load_web(url):
    web_res = requests.get(url)
    web_res.encoding = 'utf8'
    # print(job_web_res.text)
    time.sleep(random.uniform(0, 2))
    web_bs = bs(web_res.text)
    return web_bs


def writeline(array):
    wl = '"' + array[0] + '"'
    for i in range(1, len(array)):
        wl = wl + ',"' + array[i] + '"'
    return wl


def get_all_page(beautifulsoup_text):
    page = beautifulsoup_text.select('.next_page')[0]
    tt = page.text.replace('\t', '').split('\n')
    num = tt[1].find('共')
    allpage = int(tt[1][num + 2])
    return allpage


class job_class(object):

    def __init__(self, joblist):
        self.job_name = joblist.select('a')[0]['title']  # job name
        self.com_name = joblist.select('a')[1]['title']  # company name
        self.edu = joblist.select(".edu")[0].text.replace('\t', '').replace('\r\n', '')
        self.area = joblist.select(".area")[0].text.replace('\t', '').replace('\r\n', '')
        self.job_url = "https://www.104.com.tw" + joblist.select('a')[0]['href']
        self.com_url = "https://www.104.com.tw" + joblist.select('a')[1]['href']

    # job info
    def load_job_info(job_web_bs):
        job_info = {}
        main_info = job_web_bs.select("section")[0]
        title1 = main_info.select('h2')[0].text  # 工作內容
        title2 = '工作說明'
        explanation = main_info.select('p')[0].text.replace('\r', ' ')

        if title1 not in job_info.keys():
            job_info[title1] = {}
        if title2 not in job_info[title1].keys():
            job_info[title1][title2] = {}
        job_info[title1][title2] = explanation

        for i in range(len(main_info.select('dt'))):
            title2 = main_info.select('dt')[i].text.replace('\r', '').replace('\t', '').replace('：', '')
            explanation = main_info.select('dd')[i].text.replace(' ', '').replace('\n', '')
            if title2 not in job_info[title1].keys():
                job_info[title1][title2] = {}
            job_info[title1][title2] = explanation

        # job condition
        condition = job_web_bs.select("section")[1]
        title1 = condition.select('h2')[0].text  # 工作條件
        if title1 not in job_info.keys():
            job_info[title1] = {}

        for i in range(len(condition.select('dt'))):
            title2 = condition.select('dt')[i].text.replace('：', '')
            explanation = condition.select('dd')[i].text.replace(' ', '')
            if title2 not in job_info[title1].keys():
                job_info[title1][title2] = {}
            job_info[title1][title2] = explanation

        # work welfare
        welfare = job_web_bs.select("section")[2]
        title1 = welfare.select('h2')[0].text  # 公司福利
        explanation = welfare.select('p')[0].text.replace('\r\u3000', '\t').replace('\r', '')
        if title1 not in job_info.keys():
            job_info[title1] = {}
        job_info[title1] = explanation
        return job_info

    # company info
    def load_com_info(com_web_bs):
        com_info = {}
        com_info_bs = com_web_bs.select(".intro")[0]
        title1 = com_info_bs.select('h2')[0].text  # 公司介紹

        if title1 not in com_info.keys():
            com_info[title1] = {}
        for i in range(len(com_info_bs.select('dt'))):
            title2 = com_info_bs.select('dt')[i].text.replace('\u3000', '').replace('：', '')
            explanation = com_info_bs.select('dd')[i].text.replace('\r', '').replace('\n', '')
            if title2 not in com_info[title1].keys():
                com_info[title1][title2] = {}
            com_info[title1][title2] = explanation

        com_info_bs = com_web_bs.select(".intro")[1]
        title1 = com_info_bs.select('h2')[0].text  # 公司簡介
        explanation = com_info_bs.select('p')[0].text.replace('\r', '\n')
        if title1 not in com_info.keys():
            com_info[title1] = {}
        com_info[title1] = explanation

        title1 = com_info_bs.select('h2')[1].text  # 主要商品／服務項目
        explanation = com_info_bs.select('p')[1].text.replace('\r', '')
        if title1 not in com_info.keys():
            com_info[title1] = {}
        com_info[title1] = explanation
        return com_info

    # number of people apply for a job
    def num_of_people(job_web_bs):
        number_of_people_bs = job_web_bs.select('.sub')[0]
        number_of_people = number_of_people_bs.select('a')[0].text
        return number_of_people


def load_104_newpeople_main(search_url, filename='./test.csv'):
    print('write to file ', filename)

    job_list = [['', '工作內容', '條件要求', '公司福利'],
                ['工作說明', '職務類別', '工作待遇', '工作性質', '上班地點', '管理責任', '出差外派', '上班時段', '休假制度', '可上班日', '需求人數'],
                ['接受身份', '工作經歷', '學歷要求', '科系要求', '語文條件', '擅長工具', '工作技能', '具備駕照', '其他條件']]
    com_list = [['', '公司介紹', '公司簡介', '主要商品／服務項目'],
                ['產業類別', '產業描述', '員工', '資\xa0本\xa0額', '聯\xa0絡\xa0人', '公司地址', '電話', '傳真', '公司網址']]
    all_headlist = ['職務名稱', '公司名稱', '學歷', '地區', '應徵人數',
                    '工作說明', '職務類別', '工作待遇', '工作性質', '上班地點', '管理責任', '出差外派', '上班時段', '休假制度', '可上班日', '需求人數', '接受身份',
                    '工作經歷', '學歷要求', '科系要求', '語文條件', '擅長工具', '工作技能', '具備駕照', '其他條件', '公司福利',
                    '產業類別', '產業描述', '員工', '資本額', '聯絡人', '公司地址', '電話', '傳真', '公司網址', '公司簡介', '主要商品／服務項目']

    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'}

    res = requests.get(search_url, headers=head)
    # print(res.encoding)
    res.encoding = 'utf8'
    soup = bs(res.text)

    wl = writeline(all_headlist)

    fw = open(filename, 'w')
    fw.writelines(wl + '\n')

    allpage = get_all_page(soup) + 1

    for page in range(1, allpage):

        if page == 1:
            print('page:', page)
            print(search_url)

        else:
            print('page:', page)
            # url = 'https://www.104.com.tw/area/freshman/search?area=6001001000%2C6001002000&jobcategory=2007000000&industry=&keyword=%E6%A9%9F%E5%99%A8%E4%BA%BA&page=2&sortField=APPEAR_DATE&sortMode=DESC'
            findpage = 'page='
            local = search_url.find(findpage)
            tmp = list(search_url)
            tmp[local + len(findpage)] = str(page)
            search_url = ''.join(tmp)

            res = requests.get(search_url, headers=head)
            # print(res.encoding)
            res.encoding = 'utf8'
            soup = bs(res.text)
            print(search_url)

        job_box = soup.select(".job_box")[0]

        # job_url = ''
        # com_url = ''
        for joblis in job_box.select('.joblist_cont'):

            job = job_class(joblis)
            print(job.job_name)

            #        print("job_url: ", job_url)
            #        print("com url: ", com_url)
            global job_info
            global com_info
            job_web_bs = load_web(job.job_url)
            com_web_bs = load_web(job.com_url)

            # number of people apply for a job
            num = job_class.num_of_people(job_web_bs)
            # job info
            job_info = job_class.load_job_info(job_web_bs)
            # company
            com_info = job_class.load_com_info(com_web_bs)

            once_data = []
            once_data.append(job.job_name)
            once_data.append(job.com_name)
            once_data.append(job.edu)
            once_data.append(job.area)
            once_data.append(num)
            # job
            for j in range(len(job_list[1])):
                try:
                    once_data.append(job_info[job_list[0][1]][job_list[1][j]])
                except:
                    once_data.append('')
            for j in range(len(job_list[2])):
                try:
                    once_data.append(job_info[job_list[0][2]][job_list[2][j]])
                except:
                    once_data.append('')
            once_data.append(job_info[job_list[0][3]])

            # company
            for j in range(len(com_list[1])):
                try:
                    once_data.append(com_info[com_list[0][1]][com_list[1][j]])
                except:
                    once_data.append('')
            once_data.append(com_info[com_list[0][2]])
            once_data.append(com_info[com_list[0][3]])

            # do wl
            wl = writeline(once_data)
            for j in range(len(wl)):
                try:
                    wl[j].encode('cp950').decode('cp950')
                except:
                    tmp = list(wl)
                    tmp[j] = " "
                    wl = ''.join(tmp)
            # write to file
            fw.writelines(wl + '\n')
            break

    fw.close()
    print('output file succesful')
    return 'succesful'


if __name__ == '__main__':
    filename = './test.csv'
    search_url = "https://www.104.com.tw/area/freshman/search?keyword=%E6%A9%9F%E5%99%A8%E4%BA%BA&area=6001001000,6001002000&jobcategory=2007000000&industry=&page=1&sortField=APPEAR_DATE&sortMode=DESC"

    load_104_newpeople_main(search_url, filename)