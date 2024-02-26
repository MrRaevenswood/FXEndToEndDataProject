from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from lxml import etree

import pandas as pd

def getTradingEconomicsCurrencyForecasts(url):
    options = Options()
    options.headless = True

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
        "prefs", {"profile.managed_default_content_settings.images":2}
    )

    driver = webdriver.Chrome()
    driver.get(url)

    element = WebDriverWait(driver=driver, timeout=5).until(
        EC.presence_of_element_located((By.XPATH,"//div[@class='table-responsive']"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    dom = etree.HTML(str(soup))

    thValues = ["Major","Price","Signal","Q1/24","Q2/24","Q3/24","Q4/24"]
    titles = dom.xpath("//table[@class='table table-hover table-striped']/tbody/tr/td[@class='datatable-item-first']/a/b/text()")

    currentPrices = dom.xpath("//table[@class='table table-hover table-striped']/tbody/tr/td[@id='p']/text()")
    futurePrices = dom.xpath("//table[@class='table table-hover table-striped']/tbody/tr/td[@style='text-align: center;']/text()")
    signals = dom.xpath("//table[@class='table table-hover table-striped']/tbody/tr/td[@class='datatable-item']/span/@title")

    parsed = []
    for title in titles:
        parsed.append({
            thValues[0]: title,
            thValues[1]: currentPrices.pop(0).strip(),
            thValues[2]: signals.pop(0).strip(),
            thValues[3]: futurePrices.pop(0).strip(),
            thValues[4]: futurePrices.pop(0).strip(),
            thValues[5]: futurePrices.pop(0).strip(),
            thValues[6]: futurePrices.pop(0).strip()
        })

    tradingEconomicsForecastDf = pd.DataFrame(parsed)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(tradingEconomicsForecastDf)

getTradingEconomicsCurrencyForecasts("https://tradingeconomics.com/forecast/currency")
