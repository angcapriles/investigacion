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
        self.url = 'https://www.scopus.com/freelookup/form/author.uri'
        self.load_page()

    def load_page(self):
        try:
            opts = Options()
            opts.add_argument("no-sandbox")
            opts.add_argument("--headless")
            opts.add_argument("--disable-extensions")
            self.driver = webdriver.Firefox(
                executable_path='/bin/firefox_driver/geckodriver')
        except:
            opts = Options()
            opts.add_argument("no-sandbox")
            opts.add_argument("--headless")
            opts.add_argument("--disable-extensions")
            self.driver = webdriver.Firefox(
                executable_path=".\geckodriver.exe")
        self.driver.get(self.url)

    def _catch_element_or_not(self, element, type=0):
        if type == 2:
            try:
                result = self.driver.find_elements_by_xpath(element)
            except Exception as e:
                print(e)
                result = "NA"
        else:
            try:
                result = self.driver.find_element_by_xpath(element).text

            except Exception as e:
                print(e)
                result = "NA"

        return result

    def get_profile(self, orcid):
        if orcid != "NA":
            time.sleep(10)
            try:
                self.driver.execute_script(
                    "document.getElementById('orcidId').value='"+orcid+"'")
                print(orcid)
                self.driver.find_element_by_xpath(
                    '//*[@id = "orcidSubmitBtn"]').click()
            except Exception as e:
                print(e)
                print("==== Script finalizado por fallas en la conexion.")
                self.close_all()
            time.sleep(10)

            try:
                self.driver.find_element_by_class_name('docTitle').click()
                time.sleep(5)
            except Exception as e:
                print(e)
                print("==== ORCID no genero resultados.")
                self.driver.back()
                time.sleep(5)
                return

            name = self._catch_element_or_not('//*[@class="wordBreakWord"]')

            full_data_uni = self._catch_element_or_not(
                '//*[@id="firstAffiliationInHistory"]')
            if full_data_uni != "NA":
                full_data_uni = full_data_uni.split(',')

                univ = full_data_uni[0]
                country = full_data_uni[-1].split('View')[0]
            else:
                univ = "NA"
                country = "NA"

            areas = self._catch_element_or_not(
                '//*[@id="subjectAreaBadges"]/span', 2)
            if areas != "NA":
                areas_list = []
                for area in areas:
                    areas_list.append(area.text)
                areas = ', '.join(areas_list)

            doc_by_author = self._catch_element_or_not(
                '//*[@id="authorDetailsDocumentsByAuthor"]/div[2]/div/span')

            cite_by_doc = self._catch_element_or_not(
                '//*[@class="resultsCountCite"]')

            total_cite = self._catch_element_or_not(
                '//*[@id="totalCiteCount"]')

            h_index = self._catch_element_or_not(
                '//*[@id="authorDetailsHindex"]/div[2]/div/span')

            # Writing the result to csv file
            with open('profile_scopus.csv', 'a', encoding="utf-8") as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(
                    [name, univ, country, areas, doc_by_author, total_cite, h_index, cite_by_doc])
            csvFile.close()

            print("Return 2 pages")
            self.driver.execute_script("window.history.go(-2)")
            time.sleep(10)

            try:
                time.sleep(5)
                self.driver.find_element_by_xpath(
                    '//*[@id = "_pendo-close-guide_"]').click()
            except:
                pass

        else:
            print(orcid)

    def reload_page(self):
        self.close_all()
        self.load_page()
        time.sleep(10)

    def close_all(self):
        self.driver.execute_script('window.close()')
        self.driver.close()


if __name__ == "__main__":
    print("### Script Began ###")
    schopus = Schopus()

    col = ['Nombre', 'Universidad', 'País', 'Areas', 'Documentos por  autor',
           'Total de citas', 'H-Index', 'Citas por documento']
    with open('profile_scopus.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col)

    f = open('result2.csv', encoding="utf8")
    readFile = csv.reader(f)
    readFile = iter(readFile)
    next(readFile)
    index = 0
    for row in readFile:
        schopus.get_profile(row[2].lstrip())
        if index == 40:
            print("==== Reload page")
            schopus.reload_page()
            index = 0
        else:
            index += 1

    schopus.close_all()
    print("## End ##")
