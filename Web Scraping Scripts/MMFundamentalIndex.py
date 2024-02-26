from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from lxml import etree

import pandas as pd

def getMMFundamentalIndexData(url):
    options = Options()
    options.headless = True

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
        "prefs", {"profile.managed_default_content_settings.images":2}
    )

    driver = webdriver.Chrome()
    driver.get(url)

    driver.execute_script("window.scrollTo(0, 300);")

    element = WebDriverWait(driver=driver, timeout=50).until(
        EC.presence_of_element_located((By.XPATH,"//div[@class='mm-cc-chart-title']"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    dom = etree.HTML(str(soup))

    thValues = ["Index Name","Index Value","Date"]
    indexName = dom.xpath("//div[@class='sidebar-sec chart-stat-lastrows']/ul/li/div[@class='stat-name']/span/text()")
    indexValues = dom.xpath("//div[@class='sidebar-sec chart-stat-lastrows']/ul/li/div[@class='stat-val']/span[@class='val']/text()")    
    dates = dom.xpath("//div[@class='sidebar-sec chart-stat-lastrows']/ul/li/div[@class='date-label']/text()")

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    parsed = []
    for indexName in indexName:
        parsed.append({
            thValues[0]: indexName,
            thValues[1]: indexValues.pop(0).strip(),
            thValues[2]: dates.pop(0).strip()
        })

    mmFundamentalIndexDf = pd.DataFrame(parsed)
    print(mmFundamentalIndexDf)

getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/444/us-mm-gspc")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/725/tw-mm-twse")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/824/mm-sse-composite-fundamental-index")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/2108/mm-eur-index")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/1108/mm-japan-stock-fundamental-index-plot")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/3606/mm-australia-stock-fundamental-index")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/38638/mm-emerging-market-index-2020")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/2195/mm-india-index")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/2593/mm-ibov-index")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/1736/mm-rts-index")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/763/mm-us-bond-index")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/36943/mm-ig-bond-index-2020")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/36944/mm-hy-bond-index-2020")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/14948/mm-dxy-expectation-index")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/38394/mm-gbp-fundamental-Index")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/17880/mm-euro-expectation-index")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/1078/mm-taiwan-dollars-basic-index")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/74812/mm-jpy-index-2020-vs-jpy")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/182/mm-oil-expectation-index")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/749/mm-gold")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/27102/mm-silver-index")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/961/mm-copper-fundamental-index")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/767/mm-soybean-index")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/765/mm-wheat-index")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/766/mm-corn-index")
getMMFundamentalIndexData("https://en.macromicro.me/collections/6502/mm-fundamental-index/28287/mm-cotton-index")
