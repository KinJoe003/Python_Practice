# coding=utf-8
import requests
from bs4 import BeautifulSoup
import csv
import random, time


url_A = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=python&order=15&asc=0&page='
url_B = '&mode=s&jobsource=2018indexpoc'
headers = {
    "Referer": "https://www.104.com.tw/jobs/search/?",
}

all_job_datas = []
for page in range(1, 10 + 1):
    url = url_A + str(page) + url_B
    print(url)
    htmlFile = requests.get(url)
    ObjSoup = BeautifulSoup(htmlFile.text, 'html.parser')
    jobs = ObjSoup.find_all('article', class_='js-job-item')  # 搜尋所有職缺

    for job in jobs:
        job_name = job.find('a', class_="js-job-link").text  # 職缺內容
        job_company = job.get('data-cust-name')  # 公司名稱
        job_des = job.find('p', class_ ='job-list-item__info b-clearfix b-content').text  # 內容
        job_loc = job.find('ul', class_='job-list-intro').find('li').text  # 地址
        job_pay = job.find('span', class_='b-tag--default').text  # 薪資
        job_url = job.find('a').get('href')  # 網址
        job_data = {'職缺內容': job_name, '公司名稱': job_company,
                    '內容':job_des, '地址': job_loc, '薪資': job_pay, '網址': job_url}
        all_job_datas.append(job_data)
    time.sleep(random.randint(1, 3))

fn = '104人力銀行職缺.csv'  # 取CSV檔名
columns_name = ['職缺內容', '公司名稱', '內容', '地址', '薪資', '網址']  # 第一欄的名稱
with open(fn, 'w', newline='', encoding="utf_8_sig") as csvFile:  # 定義CSV的寫入檔,並且每次寫入完會換下一行
    dictWriter = csv.DictWriter(csvFile, fieldnames=columns_name)  # 定義寫入器
    dictWriter.writeheader()
    for data in all_job_datas:
        dictWriter.writerow(data)