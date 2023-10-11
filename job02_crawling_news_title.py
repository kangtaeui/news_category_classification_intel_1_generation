from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import time
import datetime

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'
options = ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
#options.add_argument('--no-sandbox')
#options.add_argument('window-size=1920x1080')
#options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)
driver.get(url)


pages = [110, 110, 110, 75, 110, 72]
df_titles = pd.DataFrame()



for l in range(6):
    section_url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'.format(l)
    titles =[]
    for k in range(1, pages[l]+1):
        url = section_url + '#&date=%2000:00:00&page={}'.format(k)
        driver.get(url)
        time.sleep(0.5)
        for i in range(1, 5):
            for j in range(1, 6):
                title = driver.find_element('xpath', '//*[@id="section_body"]/ul[1]/li[1]/dl/dt[2]/a'.format(i, j)).text
                title = re.compile('[^가-힣]').sub(' ', title)
                titles.append(title)
    df_section_title = pd.DataFrame(titles, columns=['titles'])
    df_section_title['category'] = category[l]
    df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
df_titles.to_csv('./crawling_data/crawling_data.csv')

print(titles.head())
df_titles.info()
print(df_titles['category'].value_counts())

