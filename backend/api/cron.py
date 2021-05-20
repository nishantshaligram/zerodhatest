import json
import os
from time import strftime, gmtime
import redis
from bs4 import BeautifulSoup
from selenium import webdriver
from download import download
import csv
from django.conf import settings

def my_cron_job():
    print("hello world")
    with open('/log/general.txt','a') as file:
            file.write('cron is called: %s\n' %strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
    # Connect to our Redis instance
    # comment below line if running project locally
    redis_instance = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True, db=0)
    # un-comment below line if running project locally
    # redis_instance = redis.Redis(host="localhost", port="6379", decode_responses=True, db=0)
    redis_instance.flushall()

    # create necessary directory
    if not os.path.isdir('downloaded'):
        os.makedirs('downloaded')
    if not os.path.isdir('log'):
        os.makedirs('log')

    # find download link in page
    website_url = "https://www.bseindia.com"
    # driver = webdriver.Chrome("backend/chromedriver.exe")
    try:
        driver = webdriver.Chrome()
        driver.get('https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx')
        html = driver.page_source
        driver.close()
        driver.quit()
    except: 
        with open('/log/chromedriver-log.txt','a') as file:
            file.write('Error Occured: %s\n' %strftime("%Y-%m-%d %H:%M:%S", gmtime()) )


    soup = BeautifulSoup(html, 'lxml')
    link = soup.find('a', {'id': 'ContentPlaceHolder1_btnhylZip'})

    zip_url = website_url + link["href"]

    filename = zip_url.split('/')[-1]

    # get zip data from url
    extracted_path = download(zip_url, 'downloaded/' + filename, kind="zip", replace=True)

    # extracted_file = extracted_path.split('/')[1]
    zipfilename = filename.split('.')[0]
    csvfile = zipfilename.split('_')[0]
    csvfilepath = extracted_path + '/' + csvfile + '.CSV'

    with open(csvfilepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                redis_instance.set(str(row[1]).lower(), json.dumps({'code': str(row[0]), 'name': str(row[1]), 'open':str(row[4]), 'high':str(row[5]), 'low': str( row[6]), 'close': str(row[7]) }))
                line_count += 1
        with open('/log/cron-log.txt','a') as file:
            file.write('Bhavcopy Updated: %s\n' %strftime("%Y-%m-%d %H:%M:%S", gmtime()) )