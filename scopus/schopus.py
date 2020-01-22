import csv
import os
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class Schopus():
    def __init__(self):
        url = 'https://www.scopus.com/freelookup/form/author.uri'
        try:
            opts = Options()
            opts.add_argument("no-sandbox")
            opts.add_argument("--headless")
            opts.add_argument("--disable-extensions")
            self.driver = webdriver.Firefox(executable_path='/bin/firefox_driver/geckodriver')
        except:
            opts = Options()
            opts.add_argument("no-sandbox")
            opts.add_argument("--headless")
            opts.add_argument("--disable-extensions")
            self.driver = webdriver.Firefox(executable_path=".\geckodriver.exe")

        print("Loading page....")
        self.driver.get(url)
    def get_profile(self, orcid):
        if orcid != "NA":
            try:
                time.sleep(10)
                self.driver.execute_script("document.getElementById('orcidId').value='"+orcid+"'")
                print(orcid)
                time.sleep(2)
                self.driver.find_element_by_xpath('//*[@id = "orcidSubmitBtn"]').click()
            except Exception as e:
                print(e)
                self.close_all()
            try:
                self.driver.find_element_by_class_name('docTitle').click()
                time.sleep(5)
            except:
                self.driver.back()
                time.sleep(5)
                return

            name = self.driver.find_element_by_class_name("wordBreakWord").text
            full_data_uni = self.driver.find_element(By.ID, "firstAffiliationInHistory").text.split(',')
            univ =  full_data_uni[0]
            country = full_data_uni[-1].split('View')[0]
            try:
                areas = self.driver.find_elements_by_xpath('//*[@id="subjectAreaBadges"]/span')
                areas_list = []
                for area in areas:
                    areas_list.append(area.text)
                areas =  ', '.join(areas_list)
            except:
                areas = "NA"
            try:
                doc_by_author = self.driver.find_element_by_xpath('//*[@id="authorDetailsDocumentsByAuthor"]/div[2]/div/span').text
            except:
                doc_by_author = "NA"
            try:
                cite_by_doc =  self.driver.find_element_by_xpath('//*[@class="resultsCountCite"]').text
            except:
                cite_by_doc = "NA"
            try:
                total_cite = self.driver.find_element_by_xpath('//*[@id="totalCiteCount"]').text
            except:
                total_cite = "NA"
            try:
                h_index = self.driver.find_element_by_xpath('//*[@id="authorDetailsHindex"]/div[2]/div/span').text
            except:
                h_index = "NA"

            try:
                # Writing the result to csv file
                with open('profile_scopus.csv', 'a') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow([name, univ, country, areas, doc_by_author, total_cite, h_index, cite_by_doc])
                csvFile.close()

                print("Return 2 pages")
                self.driver.execute_script("window.history.go(-2)")
                time.sleep(10)
            except Exception as e:
                print(e)
                self.driver.execute_script("window.history.go(-2)")
                time.sleep(10)

            try:
                time.sleep(5)
                self.driver.find_element_by_xpath('//*[@id = "_pendo-close-guide_"]').click()
            except:
                pass

        else:
            print(orcid)

    def close_all(self):
        self.driver.execute_script('window.close()')
        self.driver.close()
if __name__ == "__main__":
    print("### Script Began ###")
    schopus = Schopus()

    col = ['Nombre', 'Universidad', 'País', 'Areas', 'Documentos por  autor', 'Total de citas', 'H-Index', 'Citas por documento']
    with open('profile_scopus.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col)

    f = open('result2.csv', encoding="utf8")
    readFile = csv.reader(f)
    readFile = iter(readFile)
    next(readFile)

    print("### Script Began ###")
    for row in readFile:
        schopus.get_profile(row[2].lstrip())
    schopus.close_all()
    print("## End ##")
