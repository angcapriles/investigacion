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

class Sholar():
    def __init__(self):
        self.selected_profile = ""
        url = 'https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors='
        try:
            opts = Options()
            opts.add_argument("no-sandbox")
            opts.add_argument("--headless")
            opts.add_argument("--disable-extensions")
            self.driver = webdriver.Firefox(executable_path='./geckodriver')
        except:
            options = webdriver.ChromeOptions()
            options.add_argument("no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--disable-extensions")
            self.driver = webdriver.Chrome(executable_path=".\chromedriver.exe", options=options)
        self.driver.get(url)


    def get_profile(self, name, univ):
        try:
            self.driver.switch_to.window(self.driver.window_handles[0])
        except:
            pass
        print("------------------------------")
        print("** New profile **")
        try:
            self.driver.execute_script("document.getElementById('gs_hdr_tsi').value='"+name+"'")
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id = "gs_hdr_tsb"]').click()
        except:
            print("** No profile in the search result **")

        # Wait for search results to load
        WebDriverWait(self.driver, 30).until(
            expected_conditions.invisibility_of_element_located((By.ID, 'ajax_loader'))
        )
        time.sleep(2)
        results = self.driver.find_elements_by_xpath('//*[@id = "gsc_sa_ccl"]/div')
        print('Result number', len(results))
        try:
            links = []
            for result in results:
                if self.check_profile_link(name, univ, result):
                    links.append(result.find_element_by_tag_name('a').get_attribute('href'))
            print(links)
            for link in links:
                newTab = 'window.open("' + link + '", "_blank");'
                self.driver.execute_script(newTab)
                self.driver.switch_to.window(self.driver.window_handles[1])
                time.sleep(5)
                self.get_profile_data()
                self.driver.switch_to.window(self.driver.window_handles[0])
            print("** End **")
        except:
            print("** No results **")
    def check_profile_link(self, name, univ, result):
        check = False
        r_univ = univ.split(",")
        r_name = name.split(" ")
        name_c = result.find_element_by_class_name("gs_ai_name").text
        univ_c = result.find_element_by_class_name("gs_ai_aff").text
        print("**Profile cheking**")
        print(r_name, name_c)
        print(r_univ, univ_c)

        for name_c in r_name:
            if name_c in name:
                for univ_c in r_univ:
                    if univ_c in univ:
                        check = True
        if check:
            print("found")
            return True
        else:
            print("Not found")
            return False

    def get_profile_data(self):
        # Extraer informacion de perfil.
        try:
            self.driver.find_element_by_xpath('//*[@id = "gsc_bpf_more"]').click()
        except:
            pass
        try:
            time.sleep(20)
            # Extracting profile data
            profile = []
            name = self.driver.find_element_by_xpath('//*[@id="gsc_prf_i"]/div[1]').text
            studies = self.driver.find_element_by_xpath('//*[@id="gsc_prf_i"]/div[2]').text

            areas = self.driver.find_elements_by_xpath('//*[@id="gsc_prf_i"]/div[4]/a')
            areas_list = []
            for area in areas:
                areas_list.append(area.text)
            profile_h = self.driver.find_element_by_xpath('//*[@id="gsc_rsb_st"]/tbody/tr[2]/td[2]').text
            profile_i10 = self.driver.find_element_by_xpath('//*[@id="gsc_rsb_st"]/tbody/tr[3]/td[2]').text
            areas = ', '.join(areas_list)
            profile.extend([name, studies, areas, profile_h, profile_i10])

            # Looking for coautor
            co_autors = self.driver.find_elements_by_xpath('//*[@id="gsc_rsb_co"]/ul/li')
            for co_autor in co_autors:
                name_co_autor = co_autor.find_element_by_tag_name('a').text
                try:
                    institute_co_autor = co_autor.find_element_by_class_name('gsc_rsb_a_ext').text
                except:
                    institute_co_autor = "Not works"

                profile.extend([name_co_autor, institute_co_autor])

            # Writing the result to csv file
            with open('profiles.csv', 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(profile)
            csvFile.close()
            print(profile)
            self.driver.execute_script('window.close()')
        except:
            self.driver.execute_script('window.close()')
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.close()
    def close_all(self):
        self.driver.execute_script('window.close()')
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.close()

if __name__ == "__main__":
    scholar = Sholar()
    col = ['NOMBRE', 'UNIVERSIDAD', 'AREAS DE ESTUDIO', 'H', 'I10']
    coautor = []
    for cindex in range(20):
        name = "CO-AUTOR {}".format(cindex)
        institute = "INSTITUCION CO-AUTOR {}".format(cindex)
        col.extend([name, institute])

    with open('profiles.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col)
    f = open('result.csv', encoding="utf8")
    readFile = csv.reader(f)
    readFile = iter(readFile)
    next(readFile)
    print("### Script Began ###")
    for row in readFile:
        scholar.get_profile(row[0].lstrip(), row[1].lstrip())
