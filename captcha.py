from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from court_scraper import access_url_from_csv


def loop_through_table(driver):
    tbody = driver.find_element_by_id("showList1")
    rows = tbody.find_elements_by_xpath(".//tr")

    d = {}

    for x in range(1, len(rows)):
        last_cell = rows[x].find_elements_by_xpath(".//td[contains(@class, 'col-xs-2')]")
        btn = last_cell[0].find_elements_by_xpath(".//a")[0]
        btn.click()
        span = driver.find_elements_by_xpath("//*[contains(text(), 'Filing Date')]")[0].find_elements_by_xpath("..")[0]
        print(span.text[13:])
        d[x] = span.text[13:]
        back = driver.find_elements_by_xpath("//a[contains(@onclick, 'funBack()')]")[0]
        print(back.text)
        back.click()

    print(d)


def run_get_all_types(data):
    driver = webdriver.Firefox('./geckodriver')

    for block in data:
        driver.get(block['url'])

        fd = Select(driver.find_element_by_id('court_complex_code'))
        sd = Select(driver.find_element_by_id('case_type'))
        yi = driver.find_element_by_id("search_year")

        fd.select_by_index(1)
        sd.select_by_index(2)
        yi.send_keys('2019')

        table = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(@class, 'col-xs')]"))
        )

        loop_through_table(driver)


urls = access_url_from_csv()[:1]
#run_get_all_types(urls)
