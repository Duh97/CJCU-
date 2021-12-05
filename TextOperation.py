# -*- coding: utf-8 -*-
import monpa

from monpa import utils
from collections import Counter
from operator import itemgetter
from wordcloud import WordCloud, STOPWORDS
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

import matplotlib.pyplot as plt


# ========================================================================================================================= #
def monpaTokenization(targetString):
    tokenList = []

    for eachToken in monpa.cut(targetString.lower()):
        eachToken = eachToken.strip()

        if ' ' in eachToken:
            tokenList.extend(eachToken.split(' '))
        else:
            tokenList.append(eachToken)

    return tokenList
# ========================================================================================================================= #


# ========================================================================================================================= #
def contextTokenization(targetSentence):
    allTokens = []
    sentenceList = utils.short_sentence(targetSentence)

    for eachString in sentenceList:
        allTokens.extend(monpaTokenization(eachString))

    return allTokens
# ========================================================================================================================= #


# ========================================================================================================================= #
def monpaPOSTagging(targetString):
    posList = []

    for eachTuple in monpa.pseg(targetString.lower()):
        posList.append(eachTuple)

    return posList
# ========================================================================================================================= #


# ========================================================================================================================= #
def contextPOSTagging(targetSentence):
    allPOSList = []
    sentenceList = utils.short_sentence(targetSentence)

    for eachString in sentenceList:
        allPOSList.extend(monpaPOSTagging(eachString))

    return allPOSList
# ========================================================================================================================= #


# ========================================================================================================================= #
def calculateTokenCounts(targetTokenList):
    return dict(sorted(dict(Counter(targetTokenList)).items(), key=itemgetter(1), reverse=True))
# ========================================================================================================================= #


# ========================================================================================================================= #
def plotWordCloud(targetTokenList):
    stopWordSet = set(STOPWORDS)
    stopWordSet.add('的')
    stopWordSet.add('與')
    stopWordSet.add('及')

    wc = WordCloud(width=800, height=400, background_color='black', font_path='SimHei.ttf', stopwords=stopWordSet)
    wc.generate(' '.join(targetTokenList))
    wc.to_file('ExampleWordCloud.png')

    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()
# ========================================================================================================================= #


# ========================================================================================================================= #
def getCountMatrix(targetTokenList):
    vectorizer = CountVectorizer()
    getMatrix = vectorizer.fit_transform(targetTokenList)

    print(vectorizer.get_feature_names())

    return getMatrix.toarray()
# ========================================================================================================================= #


# ================================================================================= #
def getTFIDFMatrix(targetTokenList):
    vectorizer = TfidfVectorizer()
    getMatrix = vectorizer.fit_transform(targetTokenList)

    print(vectorizer.get_feature_names())

    return getMatrix.toarray()
# ================================================================================= #


# ========================================================================================================================= #
if __name__ == '__main__':
    #contextTokens = contextTokenization('分子醫學研究在近十年的變化與進展非常快速。隨著生物實驗及相關研究資源與日俱增下，如何透過高效能的實驗設計分析與計算方法來有效且快速地找出研究者感興趣的資訊是一件相當重要的研究議題。過去在微核糖核酸的研究中，主要以微核糖核酸之發掘及其調控標的基因之預測為主。對於了解微核糖核酸在複雜的後轉錄調控作用機制中所扮演的角色及其功能並無太大的助益。基於欲解開小分子在生物體內的完整作用機制之需求。本研究將透過高效能的計算方法與分析技術並整合多項異質微陣列生物晶片等資訊，在特定的生物條件實驗設計下，於多個微核糖核酸及基因資料中找出一群具有共同表現的微核糖核酸及其調控標的基因。進而建構出以特定功能為基礎之整合式微核糖核酸調控元件。本研究亦結合文獻探勘技術的設計以協助找出與微陣列分析結果相關的文獻資訊，及探討透過顯著性功能分析與註解及階層式功能分群法所建構的癌症微核糖核酸調控模組。並設計若干組實驗如交互作用關聯擷取實驗與評估、微核糖核酸功能性驗證與評估、標的基因功能性驗證與評估、跨組織癌症調控模組之比較及調控元件模型之合理性驗證等來說明本研究的發現與價值。故本研究的主要貢獻將協助生物學家由複雜的後轉錄調控機制中，快速且正確地取得影響生物功能或疾病產生時的重要調控資訊。')
    #print(contextPOSTagging('分子醫學研究在近十年的變化與進展非常快速。隨著生物實驗及相關研究資源與日俱增下，如何透過高效能的實驗設計分析與計算方法來有效且快速地找出研究者感興趣的資訊是一件相當重要的研究議題。過去在微核糖核酸的研究中，主要以微核糖核酸之發掘及其調控標的基因之預測為主。對於了解微核糖核酸在複雜的後轉錄調控作用機制中所扮演的角色及其功能並無太大的助益。基於欲解開小分子在生物體內的完整作用機制之需求。本研究將透過高效能的計算方法與分析技術並整合多項異質微陣列生物晶片等資訊，在特定的生物條件實驗設計下，於多個微核糖核酸及基因資料中找出一群具有共同表現的微核糖核酸及其調控標的基因。進而建構出以特定功能為基礎之整合式微核糖核酸調控元件。本研究亦結合文獻探勘技術的設計以協助找出與微陣列分析結果相關的文獻資訊，及探討透過顯著性功能分析與註解及階層式功能分群法所建構的癌症微核糖核酸調控模組。並設計若干組實驗如交互作用關聯擷取實驗與評估、微核糖核酸功能性驗證與評估、標的基因功能性驗證與評估、跨組織癌症調控模組之比較及調控元件模型之合理性驗證等來說明本研究的發現與價值。故本研究的主要貢獻將協助生物學家由複雜的後轉錄調控機制中，快速且正確地取得影響生物功能或疾病產生時的重要調控資訊。'))

    #print(calculateTokenCounts(contextTokens))
    #plotWordCloud(contextTokens)

    print(getTFIDFMatrix([
        '分子 醫學 研究 在 近 十年 的 變化 與 進展 非常 快速',
        '文字 探勘 技術 是 人工 智慧 的 應用 分支 之一 透過 探勘 可 挖掘 出 更多 有 意義 的 資訊',
        '資料 探勘 技術 應用 於 分子 醫學 研究 是 個 新 顯學 文字 分析 技術 可 協助 找出 潛在 致病 因子'
    ]))
# ========================================================================================================================= #
