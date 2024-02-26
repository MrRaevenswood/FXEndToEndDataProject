from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from lxml import etree

import pandas as pd

def getDailyFXSentiment(url):
    options = Options()
    options.headless = True

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
        "prefs", {"profile.managed_default_content_settings.images":2}
    )

    driver = webdriver.Chrome()
    driver.get(url)

    element = WebDriverWait(driver=driver, timeout=5).until(
        EC.presence_of_element_located((By.XPATH,"//div[@class='d-flex flex-column']"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    dom = etree.HTML(str(soup))

    thValues = ["Symbol","Sentiment","Net Long","Net Short","Daily Change Longs","Daily Change Shorts", "Daily Change OI"]
    titles = dom.xpath("//div[@class='d-flex flex-column']/div/div/div/a[@data-sort-column='symbol']/text()")

    sentiments = dom.xpath("//div[@class='d-flex flex-column']/div/div/div/span[@data-sort-column='sentiment']/text()")
    netLongs = dom.xpath("//div[@class='d-flex flex-column']/div/div/div/div[@class='dfx-technicalSentimentCard__netLongContainer']/span[@data-type='long-value-info']/@data-value")
    netShorts = dom.xpath("//div[@class='d-flex flex-column']/div/div/div/div[@class='dfx-technicalSentimentCard__netShortContainer']/span[@data-type='short-value-info']/@data-value")

    dailyChangeLongs = dom.xpath("//div[@class='d-flex flex-column']/div/div/div[@class='dfx-technicalSentimentCard__changeDailyContainer w-100']/div/div[@class='dfx-technicalSentimentCard__change dfx-technicalSentimentCard__change--border']/span[@data-sort-column='daily-change-longs']/text()")
    dailyChangeShorts = dom.xpath("//div[@class='d-flex flex-column']/div/div/div[@class='dfx-technicalSentimentCard__changeDailyContainer w-100']/div/div[@class='dfx-technicalSentimentCard__change dfx-technicalSentimentCard__change--border']/span[@data-sort-column='daily-change-shorts']/text()")
    dailyChangeOI = dom.xpath("//div[@class='d-flex flex-column']/div/div/div[@class='dfx-technicalSentimentCard__changeDailyContainer w-100']/div/div[@class='dfx-technicalSentimentCard__change']/span[@data-sort-column='daily-change-oi']/text()")

    parsed = []
    for title in titles:
        parsed.append({
            thValues[0]: title.strip(),
            thValues[1]: sentiments.pop(0).strip(),
            thValues[2]: netLongs.pop(0).strip(),
            thValues[3]: netShorts.pop(0).strip(),
            thValues[4]: dailyChangeLongs.pop(0).strip(),
            thValues[5]: dailyChangeShorts.pop(0).strip(),
            thValues[6]: dailyChangeOI.pop(0).strip()
        })

    dailyFXSentimentDf = pd.DataFrame(parsed)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(dailyFXSentimentDf)
    
getDailyFXSentiment("https://www.dailyfx.com/sentiment")