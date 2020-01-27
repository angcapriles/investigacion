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
        self.url = 'https://publons.com/search/'
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

    def get_summary(self):
        time.sleep(10)

        publications = self._catch_element_or_not(
            "//*[@class = 'researcher-card-metrics left-bar-figures']/div[1]/p")

        total_times_cited = self._catch_element_or_not(
            "//*[@class = 'researcher-card-metrics left-bar-figures']/div[2]/p")

        h_index = self._catch_element_or_not(
            "//*[@class = 'researcher-card-metrics left-bar-figures']/div[3]/p")
        if h_index != "NA" and h_index != "-" :
            clean_h_index = re.findall("\d+", h_index)[0]
        else:
            clean_h_index = "NA"
            

        verified_reviews = self._catch_element_or_not(
            "//*[@class = 'researcher-card-metrics left-bar-figures']/div[4]/p")

        verified_editor_records = self._catch_element_or_not(
            "//*[@class = 'researcher-card-metrics left-bar-figures']/div[5]/p")
        time.sleep(10)

        return [publications, total_times_cited,
                clean_h_index, verified_reviews, verified_editor_records]

    def get_metric(self):
        try:
            self.driver.find_element_by_xpath(
                '//*[@class = "researcher-profile-page-navigation-link researcher-profile-page-backbone-link"]').click()
            time.sleep(5)
        except Exception as e:
            print(e)

        p_m_pub_in_web_science = self._catch_element_or_not(
            '//*[@class = "individual-stats"]/div[3]/div[1]/div/div[2]/p')

        p_m_sum_times_cited = self._catch_element_or_not(
            '//*[@class = "individual-stats"]/div[3]/div[2]/div/div[2]/p')

        p_m_index_h = self._catch_element_or_not(
            '//*[@class = "individual-stats"]/div[3]/div[3]/div/div[2]/p')
        if p_m_index_h != "NA" and p_m_index_h != "-":
            pm_m_clean_h_index = re.findall("\d+", p_m_index_h)[0]
        else:
            pm_m_clean_h_index = "NA"

        p_m_average_citations_per_item = self._catch_element_or_not(
            '//*[@class = "individual-stats"]/div[3]/div[4]/div/div[2]/p')

        p_m_average_citations_per_year = self._catch_element_or_not(
            '//*[@class = "individual-stats"]/div[3]/div[5]/div/div[2]/p')

        time.sleep(10)
        self.driver.back()
        time.sleep(5)

        return [p_m_pub_in_web_science, p_m_sum_times_cited, pm_m_clean_h_index, p_m_average_citations_per_item, p_m_average_citations_per_year]

    def get_profile(self, rsid):
        if rsid != "NA":
            time.sleep(10)
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
            except Exception as e:
                print(e)
                self.id_no_found(rsid)
                print("=== No result for the search")
                self.driver.back()
                time.sleep(10)
                return

            area_institution = self._catch_element_or_not(
                "//*[@class = 'researcher-card-institution']/p/a")

            summary = self.get_summary()


            metrics = self.get_metric()

            try:
                data_to_csv = [name, area_institution]
                data_to_csv.extend(summary)
                data_to_csv.extend(metrics)
                time.sleep(5)
                # Writing the result to csv file
                with open('profile_publons.csv', 'a') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(data_to_csv)
                csvFile.close()
                print("==== This profile was written to the csv.")
                self.driver.back()
                time.sleep(10)
            except Exception as e:
                print(e)
                self.id_no_found(rsid)
                self.driver.back()
                time.sleep(10)
        else:
            print(rsid)

    def id_no_found(self, rsid):
        with open('untraked_profile_publons.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([rsid])
            
    def reload_page(self):
        self.close_all()
        self.load_page()
        time.sleep(10)

    def close_all(self):
        self.driver.execute_script('window.close()')
        self.driver.close()


if __name__ == "__main__":
    print("### Script Began ###")
    publons = Publons()

    col = ['Nombre', 'Area - Institucion', 'Publications',
           'Total times cited', 'H-Index', 'Verified reviews', 'Verified editor records', 'P.M. Publications in Web of Science', 'P.M. Sum of times cited', 'P.M. H-Index', 'P.M. Average citations per item', 'P.M. Average citations per year']

    with open('untraked_profile_publons.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)

    with open('profile_publons.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col)

    f = open('result2.csv', encoding="utf8")
    readFile = csv.reader(f)
    readFile = iter(readFile)
    next(readFile)
    print("### Script Begin ###")
    index = 0
    ready = []
    for row in readFile:
        if row[1].lstrip() not in ready:
            publons.get_profile(row[1].lstrip())
            if index == 40:
                print("==== Reload page")
                publons.reload_page()
                index = 0
            else:
                index += 1
            ready.append(row[1].lstrip())

    publons.close_all()
    print("## End ##")
