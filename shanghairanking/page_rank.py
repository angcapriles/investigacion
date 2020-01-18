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
        url = 'http://www.shanghairanking.com/arwu2019.html'
        try:
            opts = Options()
            opts.add_argument("no-sandbox")
            #opts.add_argument("--headless")
            opts.add_argument("--disable-extensions")
            self.driver = webdriver.Firefox(executable_path='./geckodriver')

        except:
            options = webdriver.ChromeOptions()
            options.add_argument("no-sandbox")
            #options.add_argument("--headless")
            options.add_argument("--disable-extensions")
            self.driver = webdriver.Chrome(executable_path=".\chromedriver.exe", options=options)
        print("Loading page....")
        self.driver.get(url)
    def get_page_data(self):
        university_ranking_list = self.driver.find_elements_by_xpath('//*[@id="UniversityRanking"]/tbody/tr')
        for uni_r in university_ranking_list:
            try:
                w_r = uni_r.find_element_by_xpath('td[1]').text
                inst = uni_r.find_element_by_xpath('td[2]').text
                country = uni_r.find_element_by_xpath('td[3]').find_element_by_tag_name('a').get_attribute('href').split('2019')[1].split('.')[0].replace('/', '')
                n_rank = uni_r.find_element_by_xpath('td[4]').text
                total_score = uni_r.find_element_by_xpath('td[4]').text
                # Writing the result to csv file
                with open('rank_page.csv', 'a') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow([w_r, inst, country, n_rank, total_score])
                csvFile.close()
            except:
                pass
if __name__ == "__main__":
    print("### Script Began ###")
    page_rank = PageRank()
    col = ['World Rank', 'Institution', 'País', 'National/Regional Rank', 'Total Score']
    with open('rank_page.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col)
    page_rank.get_page_data()
    print("## End ##")
