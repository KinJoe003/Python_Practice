import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.104.com.tw/jobs/search/?keyword=MySQL&order=1&jobsource=2018indexpoc&ro=0'
headers = {
    "Referer": "https://www.104.com.tw/jobs/search/?keyword=MySQL&order=1&jobsource=2018indexpoc&ro=0",
}

htmlFile = requests.get(url)
ObjSoup = BeautifulSoup(htmlFile.text, 'html.parser')
jobs = ObjSoup.find_all('article', class_='js-job-item')  # 搜尋所有職缺

fn = '104人力銀行職缺內容.csv'  # 取CSV檔名
columns_name = ['職缺內容', '公司名稱', '地址', '薪資', '內容', '網址']  # 第一欄的名稱
with open(fn, 'w', newline='', ) as csvFile:  # 定義CSV的寫入檔,並且每次寫入完會換下一行
    dictWriter = csv.DictWriter(csvFile, fieldnames=columns_name)  # 定義寫入器
    dictWriter.writeheader()

    for job in jobs:
        job_name = job.find('a', class_="js-job-link").text  # 職缺內容
        job_company = job.get('data-cust-name')  # 公司名稱
        job_des = job.find('P', class_ ='job-list-item__info')  # 職能內容
        job_loc = job.find('ul', class_='job-list-intro').find('li').text  # 地址
        job_pay = job.find('span', class_='b-tag--default').text  # 薪資
        job_url = job.find('a').get('href')  # 網址

        dictWriter.writerow({'職缺內容': job_name, '公司名稱': job_company,
                             '地址': job_loc, '薪資': job_pay, '內容':job_des, '網址': job_url})