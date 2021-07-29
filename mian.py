from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

# 爬取即將上映電影列表
url = "https://movies.yahoo.com.tw/movie_comingsoon.html?page=1"
PATH = "D:\OneDrive\Development\Tools\chromedriver.exe"

driver = webdriver.Chrome(PATH)
driver.get(url)


def get_soup():
    '''
    說明：使用BeautifulSoup取得網頁原始碼，找到我們要的網頁element後回傳
    '''
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # 找到網頁中即將上映的每部電影div，用for loop列出每一部電影的中英文片名、期待度、上映日期等資訊：
    return soup.select(".release_info_text")


def get_info(release_list_element):
    '''
    說明：將get_soup()取得的資料丟進來進行處理，這部分是Day-4寫的程式碼，針對單一頁面抓取資料
    '''
    for item in release_list_element:
        film_name_ch = item.findChildren("a")[0].text.strip()
        film_name_en = item.findChildren("a")[1].text.strip()
        try:
            expectation = item.findChild(class_="leveltext").text.split()[0]
        except:
            expectation = "無資料"
        release_time = item.findChild(class_="release_movie_time").text.split("：")[1]
        rows.append([film_name_ch, film_name_en, expectation, release_time])


# 從共有幾筆資料判斷需要點幾次下一頁：
# 網頁中取得的字串會像是"共53筆，目前顯示1~10筆"，用split()和strip()方法取得字串中間的數字後，轉為integer進行判斷
data_num_element = driver.find_element_by_xpath('//*[@id="content_l"]/div[3]/div/p')
data_num = int(data_num_element.text.split("，")[0].strip("共").strip("筆"))
repeat = (data_num // 10)

# 先建一個空的List，把所有電影資料存在rows這個List中，重複數次取得所有的即將上映電影，for loop處理完後要多執行一次讀取最後一頁的資料
rows = []
for i in range(repeat):
    get_info(get_soup())
    driver.find_element_by_xpath('//*[@id="content_l"]/div[4]/ul/li[9]/a').click()
    time.sleep(2)
get_info(get_soup())

# 將取得的所有資料存成DataFrame的表格格式後，再存成csv檔案，編碼選擇utf_8_sig就可以避免亂碼了
df = pd.DataFrame(rows, columns=["中文片名", "英文片名", "期待度", "上映日期"])
# print(df)
df.to_csv("即將上映.csv", encoding="utf_8_sig", index=False)
