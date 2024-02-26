from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from lxml import etree

import pandas as pd

def getFXStreetSentimentData(url, symbol):
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
        EC.presence_of_element_located((By.XPATH,"//div[@class='fxs_gauge_container']"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    dom = etree.HTML(str(soup))

    thValues = ["Symbol","Period","AvgPrice","Bullish","Bearish","Sideways","Bias"]
    periods = ["1 Week", "1 Month", "1 Quarter"]
    
    avgPrices = dom.xpath("//div[@class='fxs_gauge_container']/div[@class='fxs_insideChart_centered_legend']/span[@class='fxs_widget_custom_data_lable']/text()")
    bullish = dom.xpath("//div[@class='fxs_widget_avg_col']/ul[@class='forecast_results_list']/li/span[@class='fxs_txt_success_clr fxs_widget_custom_bold']/text()")
    bearish = dom.xpath("//div[@class='fxs_widget_avg_col']/ul[@class='forecast_results_list']/li/span[@class='fxs_txt_error_clr fxs_widget_custom_bold']/text()")
    sideways = dom.xpath("//div[@class='fxs_widget_avg_col']/ul[@class='forecast_results_list']/li/span[@class='fxs_txt_light_1_clr fxs_widget_custom_bold']/text()")
    bias = dom.xpath("//div[@class='fxs_widget_avg_col']/div/span[@class='fxs_widget_custom_bold']/text()")

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    parsed = []
    for period in periods:
        parsed.append({
            thValues[0]: symbol,
            thValues[1]: period,
            thValues[2]: avgPrices.pop(0).strip(),
            thValues[3]: bullish.pop(0).strip(),
            thValues[4]: bearish.pop(0).strip(),
            thValues[5]: sideways.pop(0).strip(),
            thValues[6]: bias.pop(0).strip()
        })

    fxStreetDf = pd.DataFrame(parsed)
    print(fxStreetDf)

getFXStreetSentimentData("https://www.fxstreet.com/rates-charts/eurusd/forecast","EUR/USD")
getFXStreetSentimentData("https://www.fxstreet.com/rates-charts/gbpusd/forecast","GBP/USD")
getFXStreetSentimentData("https://www.fxstreet.com/rates-charts/usdjpy/forecast","USD/JPY")
getFXStreetSentimentData("https://www.fxstreet.com/rates-charts/usdchf/forecast","USD/CHF")
getFXStreetSentimentData("https://www.fxstreet.com/rates-charts/audusd/forecast","AUD/USD")
getFXStreetSentimentData("https://www.fxstreet.com/rates-charts/nzdusd/forecast","NZD/USD")
getFXStreetSentimentData("https://www.fxstreet.com/rates-charts/usdcad/forecast","USD/CAD")
getFXStreetSentimentData("https://www.fxstreet.com/rates-charts/gbpjpy/forecast","GBP/JPY")
getFXStreetSentimentData("https://www.fxstreet.com/rates-charts/eurjpy/forecast","EUR/JPY")
getFXStreetSentimentData("https://www.fxstreet.com/rates-charts/eurgbp/forecast","EUR/GBP")
getFXStreetSentimentData("https://www.fxstreet.com/rates-charts/btcusd/forecast","BTC/USD")
getFXStreetSentimentData("https://www.fxstreet.com/rates-charts/xauusd/forecast", "XAU/USD")
getFXStreetSentimentData("https://www.fxstreet.com/rates-charts/westtexasintermediate/forecast","WTI US OIL")






