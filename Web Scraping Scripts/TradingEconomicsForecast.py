from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from lxml import etree

import pandas as pd

def getTradingEconomicsForecast(url):
    options = Options()
    options.headless = True

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
        "prefs", {"profile.managed_default_content_settings.images":2}
    )

    driver = webdriver.Chrome()
    driver.get(url)

    element = WebDriverWait(driver=driver, timeout=5).until(
        EC.presence_of_element_located((By.XPATH,"//div[@class='table-responsive card']"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    dom = etree.HTML(str(soup))

    thValues = ["Actual","Q1/24","Q2/24","Q3/24","Q4/24"]
    titles = dom.xpath("//div[@class='tab-content']/div[@role='tabpanel']/div[@class='table-responsive card']/table[@class='table table-hover']/tbody/tr/td/a/text()")

    tableValues = dom.xpath("//div[@class='tab-content']/div[@role='tabpanel']/div[@class='table-responsive card']/table[@class='table table-hover']/tbody/tr/td[@class='table-value']")
    tableValLst = [x.xpath("./span[@class='te-value-negative']/text()")[0] if len(x.xpath("./span[@class='te-value-negative']/text()")) > 0 else x.text for x in tableValues]
    tableValLst = ["0" if x is None else x for x in tableValLst]

    parsed = []
    for title in titles:
        if title.strip() == "":
            continue
        else:  
            parsed.append({
                "title": title.strip(),
                thValues[0]: tableValLst.pop(0).strip(),
                thValues[1]: tableValLst.pop(0).strip(),
                thValues[2]: tableValLst.pop(0).strip(),
                thValues[3]: tableValLst.pop(0).strip(),
                thValues[4]: tableValLst.pop(0).strip()
            })

    tradingEconomicsForecastDf = pd.DataFrame(parsed)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(tradingEconomicsForecastDf)

getTradingEconomicsForecast("https://tradingeconomics.com/united-states/forecast")
getTradingEconomicsForecast("https://tradingeconomics.com/euro-area/forecast")
