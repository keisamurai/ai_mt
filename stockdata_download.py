#///////////////////////////////////////
#// name: stockdata_download.py
#// description: ウェブページから株価情報を
#//  スクリプト配置フォルダにダウンロードする
#// conditions: スクリプト配置フォルダに
#//  銘柄情報のcsvファイルが配置されていること
#///////////////////////////////////////
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import os

#//////////////////
#// parameter
#//////////////////
CHROME_DRIVER_PATH = "C:/chromedriver_win32/chromedriver.exe"
URL_BASE = "https://kabuoji3.com/stock/"
WAIT_SEC = 10
# カレントディレクトリを取得
cwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(cwd)

#//////////////////
#// main process 
#//////////////////
# csv 読み込み
csv_file = open("Core30_SJIS_withHeader.csv", "r", encoding="ms932", errors="", newline="")
# リスト形式
f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
print("/////Start Data Download .../////")
# chromeドライバ取得
driver = webdriver.Chrome(CHROME_DRIVER_PATH)
header = next(f)
print(header)
for row in f:
    # url作成
    url = URL_BASE + str(row[0]) + '/' + '2018' + '/'
    driver.get(url)
    driver.implicitly_wait(WAIT_SEC)
    driver.find_element_by_xpath('//*[@id="base_box"]/div/div[3]/form/button').click()
    driver.implicitly_wait(WAIT_SEC)
    driver.find_element_by_xpath('//*[@id="base_box"]/div/div[3]/form/button').click()
    driver.implicitly_wait(WAIT_SEC)

# クローズ処理
driver.close()