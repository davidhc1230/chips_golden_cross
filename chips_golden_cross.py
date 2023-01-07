#因台股揭露的籌碼資訊很多，籌碼集中度是其中一種判斷未來是否具上漲(下跌)潛力的方式
#本程式以玩股網(wantgoo，https://www.wantgoo.com)爬取5日籌碼及20日籌碼集中度
#並挑選近一日之5日籌碼集中大大於20日，且5日及20日籌碼集中度皆大於0，以及成交量大於800張者
#由於挑選出之標的只能顯示其未來短線上漲機率較大，並不具有任何保證，特此聲明

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

stock_list = pd.read_csv('上市及上櫃公司代碼.csv', header=None) #讀取上市及上櫃公司代碼

stock_list = list(stock_list.iloc[:, 0]) #設為矩陣
list_n =[]
###################讀取每檔股票的籌碼資訊，並進行篩選、計算#########################
for n in stock_list:
  print(n) #顯示跑到哪一檔
  headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
  url = 'https://www.wantgoo.com/stock/' + str(n) + '/major-investors/main-trend'
  options = Options()
  options.add_argument('--log-level=3') #不輸出log
  options.add_argument('--disable-gpu') #windows必須加入此行
  webdriver_path = 'D:\暫存\python實驗室\driver\chromedriver.exe'
  driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
  driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
      Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
      })
    """
  })
  driver.get(url)
  sleep(4)

  chips_5 = driver.find_elements_by_css_selector('tr td:nth-child(5)') #5日籌碼集中度
  chips_20 = driver.find_elements_by_css_selector('tr td:nth-child(6)') #20日籌碼集中度
  
  volume = float(driver.find_element_by_css_selector('#quotesUl li:nth-child(5) span').text.replace(',','')) #成交量
  chips_5_td = float(driver.find_elements_by_css_selector('tr td:nth-child(5)')[0].text.strip('%')) #今日5日籌碼集中度
  chips_5_yd = float(driver.find_elements_by_css_selector('tr td:nth-child(5)')[1].text.strip('%')) #昨日5日籌碼集中度
  chips_20_td = float(driver.find_elements_by_css_selector('tr td:nth-child(6)')[0].text.strip('%')) #今日20日籌碼集中度
  chips_20_yd = float(driver.find_elements_by_css_selector('tr td:nth-child(6)')[1].text.strip('%')) #今日20日籌碼集中度
######挑選近一日之5日籌碼集中大大於20日，且5日及20日籌碼集中度皆大於0，以及成交量大於800張者######
  if chips_5_td > chips_5_yd and chips_20_td > chips_20_yd and chips_5_td > 0 and chips_20_td > 0 and volume >= 800 :
    final_list = []
    list_golden = []
    n = str(n)
    goldenday = 0
    for j, k in zip(chips_5, chips_20):
      j = float(j.text.strip('%'))
      k = float(k.text.strip('%'))
      if j <= k : #5日籌碼集中大大於20日
        break
      goldenday += 1
    if goldenday == 1: #近一日之5日籌碼集中大大於20日
      list_n.append(n)
      list_combine = pd.DataFrame(list_n, columns = ['代號'])
      final_list.append(list_combine)
      df_final = pd.concat(final_list)
      df_final.to_csv('chips_golden_corss.csv', sep = ',', index=False, encoding='utf_8_sig') #輸出csv
  driver.close()