# -*- coding: utf-8 -*-
import json
import requests

from bs4 import BeautifulSoup

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TenlongWebCrawler(object):
    # ========================================================================================================================= #
    def crawlerInitialize(self, targetURL):
        # *************************** Chrome瀏覽器初始化設定 *************************** #
        browserOptions = Options()

        #browserOptions.add_argument('--headless')
        browserOptions.add_argument('--start-maximized')
        browserOptions.add_argument('--ignore-certificate-errors')
        browserOptions.add_argument('log-level=3')   #INFO_0 / WARNING_1 / ERROR_2 / FATAL_3 / DEFAULT_0
        # ****************************************************************************** #

        self.getDriver = WebDriver(options=browserOptions, service=Service('chromedriver-V91.exe'))
        self.wait = WebDriverWait(self.getDriver, 60)

        self.getDriver.get(targetURL)
    # ========================================================================================================================= #


    # ========================================================================================================================= #
    def webScraping(self, keyEntity):
        sourceHtml = ''
        self.crawlerInitialize('https://www.tenlong.com.tw/')

        # ******************* 等待輸入框渲染完成後，輸入書籍查詢名稱 ******************* #
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/nav[1]/nav/div/form/input[2]')))
        self.getDriver.find_element(By.XPATH, '/html/body/div[3]/nav[1]/nav/div/form/input[2]').send_keys(keyEntity)
        # ****************************************************************************** #

        # ****************** 等待送出按鈕渲染完成後，點擊按鈕送出查詢 ****************** #
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/nav[1]/nav/div/form/button')))
        self.getDriver.find_element(By.XPATH, '/html/body/div[3]/nav[1]/nav/div/form/button').click()
        # ****************************************************************************** #

        # ******************* 等待查詢書籍渲染完成後，擷取網頁原始碼 ******************* #
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div[1]/div[4]/ul/li[1]')))
        sourceHtml = self.getDriver.page_source
        # ****************************************************************************** #

        self.getDriver.quit()

        self.receiveBookInformation(self.receiveBookURLs(sourceHtml))
    # ========================================================================================================================= #


    # ========================================================================================================================= #
    def receiveBookURLs(self, pageHtml):
        bookUrlList = []

        pageObj = BeautifulSoup(pageHtml, 'lxml')
        bookList = pageObj.find_all('li', class_='col-span-6 md:col-span-3 lg:col-span-2 h-full')

        for eachBook in bookList:
            bookUrlList.append(eachBook.find('a', class_='cover w-full')['href'])

        return bookUrlList
    # ========================================================================================================================= #


    # ========================================================================================================================= #
    def receiveBookInformation(self, getBookUrl):
        completeBookInfo, eachBookInfo,  = [], {}

        baseURL = 'https://www.tenlong.com.tw'
        headerInfo = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

        for eachBook in getBookUrl:
            TenLongBookHtml = requests.get(baseURL+eachBook, headers=headerInfo)
            bookObj = BeautifulSoup(TenLongBookHtml.text, 'lxml')

            eachBookInfo['Title'] = bookObj.find('h1', class_='item-title').text.strip()

            # ****************************** 取得完整書籍資訊 ****************************** #
            bookInfoList = bookObj.find('ul', class_='item-sub-info col-span-12 sm:col-span-8 lg:col-span-9 sm:px-4').find_all('li')

            for eachInfo in bookInfoList:
                infoTitle = eachInfo.find('span', class_='info-title').text.strip()
                infoContent = eachInfo.find('span', class_='info-content').text.strip()

                if '出版商' in infoTitle:
                    eachBookInfo['Publisher'] = infoContent
                elif '出版日期' in infoTitle:
                    eachBookInfo['PublishDate'] = infoContent
                elif '售價' in infoTitle:
                    eachBookInfo['Price'] = infoContent.replace('\n', '').replace(' ', '')
                elif '頁數' in infoTitle:
                    eachBookInfo['Pages'] = infoContent
                elif 'ISBN' in infoTitle and 'ISBN-13' not in infoTitle:
                    eachBookInfo['ISBN'] = infoContent
                else:
                    pass
            # ****************************************************************************** #

            completeBookInfo.append(eachBookInfo)
            eachBookInfo = {}

        # **************************** 爬取結果儲存為JSON檔 **************************** #
        with open('TenLongBookInfo.json', 'w', encoding='utf-8') as fileOut:
            json.dump(completeBookInfo, fileOut, ensure_ascii=False, indent=4)
        # ****************************************************************************** #
    # ========================================================================================================================= #


# ========================================================================================================================= #
if __name__ == '__main__':
    crawlerObj = TenlongWebCrawler()
    crawlerObj.webScraping('Text Mining')
# ========================================================================================================================= #