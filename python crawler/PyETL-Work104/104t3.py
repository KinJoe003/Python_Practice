import requests
from bs4 import BeautifulSoup

url = 'https://www.104.com.tw/jobs/search/?keyword=%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90%E5%B8%AB&order=1&jobsource=2018indexpoc&ro=0'
htmlFile = requests.get(url)
Soup = BeautifulSoup(htmlFile.text, 'html.parser')
jobs = Soup.find_all('article',class_='js-job-item')             #搜尋所有職缺

for job in jobs:
    print(job.find('a',class_="js-job-link").text)                  #職缺內容
    print(job.get('data-cust-name'))                                #公司名稱
    print(job.find('ul', class_='job-list-intro').find('li').text)  #地址
    print(job.find('span',class_='b-tag--default').text)            #薪資
    print(job.find('a').get('href'))                                #網址
    print('='*70)