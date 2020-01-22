import csv
import os
import re
import time
# Selenium requirements
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

class Publons():
    def __init__(self):
        url = 'https://publons.com/search/'
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

        print("Loading page....")
        self.driver.get(url)

    def get_metric(self):
        self.driver.find_element_by_xpath(
            '//*[@class = "researcher-profile-page-navigation-link researcher-profile-page-backbone-link"]').click()
        time.sleep(5)
        try:
            p_m_pub_in_web_science = self.driver.find_element_by_xpath(
                '//*[@class = "individual-stats"]/div[3]/div[1]/div/div[2]/p').text
        except:
            p_m_pub_in_web_science = "NA"
        try:
            p_m_sum_times_cited = self.driver.find_element_by_xpath(
                '//*[@class = "individual-stats"]/div[3]/div[2]/div/div[2]/p').text
        except:
            p_m_sum_times_cited = "NA"
        try:
            p_m_index_h = self.driver.find_element_by_xpath(
                '//*[@class = "individual-stats"]/div[3]/div[3]/div/div[2]/p').text
            pm_m_clean_h_index = re.findall("\d+", p_m_index_h)[0]
        except:
            p_m_index_h = "NA"
        try:
            p_m_average_citations_per_item = self.driver.find_element_by_xpath(
                '//*[@class = "individual-stats"]/div[3]/div[4]/div/div[2]/p').text
        except:
            p_m_average_citations_per_item = "NA"
        try:
            p_m_average_citations_per_year = self.driver.find_element_by_xpath(
                '//*[@class = "individual-stats"]/div[3]/div[5]/div/div[2]/p').text
        except:
            p_m_average_citations_per_year = "NA"
        time.sleep(5)
        self.driver.back()
        time.sleep(2)
        return [p_m_pub_in_web_science, p_m_sum_times_cited, pm_m_clean_h_index, p_m_average_citations_per_item, p_m_average_citations_per_year]

    def get_profile(self, rsid):
        if rsid != "NA":
            time.sleep(5)
            print(rsid)
            try:
                search_input = self.driver.find_element_by_xpath(
                    '//*[@class = "textfield right-control"]/input')
            except:
                search_input = self.driver.find_element_by_xpath(
                    '//*[@class = "textfield right-control float-label"]/input')

            search_input.clear()
            search_input.send_keys(rsid)

            time.sleep(5)
            self.driver.find_element_by_xpath(
                '//*[@class = "search-button"]').click()

            try:
                name = self.driver.find_element_by_xpath(
                    "//*[@class = 'researcher-card-names']/h2").text
                area_institution = self.driver.find_element_by_xpath(
                    "//*[@class = 'researcher-card-institution']/p/a").text
            except Exception as e:
                print(e)
                print("=== No result for the search")
                self.driver.execute_script("window.history.go(-1)")
                return

            try:
                publications = self.driver.find_element_by_xpath(
                    "//*[@class = 'researcher-card-metrics left-bar-figures']/div[1]/p").text
            except:
                publications = "NA"

            try:
                total_times_cited = self.driver.find_element_by_xpath(
                    "//*[@class = 'researcher-card-metrics left-bar-figures']/div[2]/p").text
            except:
                total_times_cited = "NA"

            try:
                h_index = self.driver.find_element_by_xpath(
                    "//*[@class = 'researcher-card-metrics left-bar-figures']/div[3]/p").text
                clean_h_index = re.findall("\d+", h_index)[0]
            except:
                h_index = "NA"

            try:
                verified_reviews = self.driver.find_element_by_xpath(
                    "//*[@class = 'researcher-card-metrics left-bar-figures']/div[4]/p").text
            except:
                verified_reviews = "NA"

            try:
                verified_editor_records = self.driver.find_element_by_xpath(
                    "//*[@class = 'researcher-card-metrics left-bar-figures']/div[5]/p").text
            except:
                verified_editor_records = "NA"

            try:
                data_to_csv = [name, area_institution, publications, total_times_cited,
                                 clean_h_index, verified_reviews, verified_editor_records]
                metrics = self.get_metric()
                data_to_csv.extend(metrics)
                time.sleep(5)
                if len(metrics) > 0:
                    # Writing the result to csv file
                    with open('profile_publons.csv', 'a') as csvFile:
                        writer = csv.writer(csvFile)
                        writer.writerow(data_to_csv)
                    csvFile.close()
                    print(name, publications)
                    self.driver.back()
                    time.sleep(10)
            except Exception as e:
                print(e)
                self.driver.back()
                time.sleep(10)
        else:
            print(rsid)

    def close_all(self):
        self.driver.execute_script('window.close()')
        self.driver.close()

if __name__ == "__main__":
    print("### Script Began ###")
    publons = Publons()

    col = ['Nombre', 'Area - Institucion', 'Publications',
           'Total times cited', 'H-Index', 'Verified reviews', 'Verified editor records', 'P.M. Publications in Web of Science', 'P.M. Sum of times cited', 'P.M. H-Index', 'P.M. Average citations per item', 'P.M. Average citations per year']
    with open('profile_publons.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col)

    f = open('result2.csv', encoding="utf8")
    readFile = csv.reader(f)
    readFile = iter(readFile)
    next(readFile)
    print("### Script Began ###")
    for row in readFile:
        publons.get_profile(row[1].lstrip())

    publons.close_all()
