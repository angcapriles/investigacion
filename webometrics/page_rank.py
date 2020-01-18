from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import csv
import os
# Chrome Windows driver
from selenium.webdriver.chrome.options import Options

class PageRank():
    def __init__(self):
        url = 'https://www.webometrics.info/es/world'
        try:
            opts = Options()
            opts.add_argument("no-sandbox")
            opts.add_argument("--headless")
            opts.add_argument("--disable-extensions")
            self.driver = webdriver.Firefox(executable_path='./geckodriver')

        except:
            options = webdriver.ChromeOptions()
            options.add_argument("no-sandbox")
            #options.add_argument("--headless")
            options.add_argument("--disable-extensions")
            self.driver = webdriver.Chrome(executable_path=".\chromedriver.exe",\
                                            options=options)
        print("Loading page....")
        self.driver.get(url)
    def get_rank_data(self):
        pages_list = self.driver.find_elements_by_xpath('//*[@class="item-list"]/ul/li')
        print("Total pages -->", len(pages_list))

if __name__ == "__main__":
    print("### Script Began ###")
    page_rank = PageRank()
    col = ['Ranking', 'Universidad', 'Det.', 'País', 'Presencía', 'Impacto',
           'Apertura', 'Excelencia']
    with open('rank_page.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col)
    page_rank.get_rank_data()
