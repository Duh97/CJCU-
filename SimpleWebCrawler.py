# -*- coding: utf-8 -*-
import json
import requests

from bs4 import BeautifulSoup


# ========================================================================================================================= #
def pttWebCrawler():
    postInfo, pushList, eachPush = {}, [], {}
    headerInfo = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

    pttFoodHtml = requests.get('https://www.ptt.cc/bbs/Food/M.1638105503.A.EE1.html', headers=headerInfo)

    postObj = BeautifulSoup(pttFoodHtml.text, 'lxml')
    contextObj = postObj.find('div', class_='bbs-screen')

    # ******************************** 取得貼文標題 ******************************** #
    titleDiv = contextObj.find_all('div', class_='article-metaline')[1]
    postInfo['Title'] = titleDiv.find('span', class_='article-meta-value').text
    # ****************************************************************************** #

    # ******************************** 取得所有推文 ******************************** #
    for eachPushDiv in contextObj.find_all('div', class_='push'):
        pushStatus = eachPushDiv.find('span', class_='push-tag')
        pushComment = eachPushDiv.find('span', class_='push-content')

        eachPush['Status'] = pushStatus.text.strip()
        eachPush['Comment'] = pushComment.text[2:]

        pushList.append(eachPush)
        eachPush = {}

        eachPushDiv.decompose()
    # ****************************************************************************** #

    # **************************** 移除不必要的HTML標籤 **************************** #
    for div in contextObj.find_all('div', class_='article-metaline'):
        div.decompose()

    for div in contextObj.find_all('div', class_='article-metaline-right'):
        div.decompose()

    for div in contextObj.find_all('span', class_='f2'):
        div.decompose()
    # ****************************************************************************** #

    postInfo['Context'] = contextObj.text.strip().replace('\n', ' ').split('--')[0].strip()
    postInfo['PushInformation'] = pushList

    # **************************** 爬取結果儲存為JSON檔 **************************** #
    with open('PttFoodSinglePost.json', 'w', encoding='utf-8') as fileOut:
        json.dump(postInfo, fileOut, ensure_ascii=False, indent=4)
    # ****************************************************************************** #
# ========================================================================================================================= #


# ========================================================================================================================= #
if __name__ == '__main__':
    pttWebCrawler()
# ========================================================================================================================= #
