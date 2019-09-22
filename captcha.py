from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from court_scraper import get_case_type_urls_from_csv
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException

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
        if x == 3:
            break

    print(d)


# indices for court types
COURT_TYPE_COMPLEX = 0
COURT_TYPE_ESTABLISHMENT = 1
# global selenium driver
driver = None
# start selenium here and open pages using the url from data
def open_page_using_url(data):
   global driver
   driver = webdriver.Firefox('./geckodriver')
   for block in data:
       driver.get(block['url'])
       # fill out form with "Court Complex" option
       block['courtComplex'] = fill_out_form(COURT_TYPE_COMPLEX)
       # fill out form with "Court Complex" option
       driver.find_element_by_id('radCourtEst').click()
       block['courtEstablishment'] = fill_out_form(COURT_TYPE_ESTABLISHMENT)
   return data
# fill out the search form based on the court type
def fill_out_form(court_type):
   if court_type == COURT_TYPE_COMPLEX:
       first_dropdown = driver.find_element_by_id('court_complex_code')
   else:
       first_dropdown = driver.find_element_by_id('court_code')
   return loop_over_dropdown_options(first_dropdown)
# set the year
# can be made to loop through a list of years later
def fill_search_year_input():
   year_input_id = "search_year"
   year_input = driver.find_element_by_id(year_input_id)
   search_year = "2019"
   year_input.send_keys(search_year)
"""
Go through all combinations of dropdown options and search.
Return a dataObj of results
"""
def loop_over_dropdown_options(first_dropdown):
   data_obj = {}
   first_dropdown_children = first_dropdown.find_elements_by_xpath(".//*")
   for child_index in range(1, len(first_dropdown_children)):
       s_first_dropdown = Select(first_dropdown)
       s_first_dropdown.select_by_index(child_index)
       first_dropdown_name = s_first_dropdown.first_selected_option.text
       data_obj[first_dropdown_name] = []
       loop_over_case_type_options(data_obj[first_dropdown_name])
       if child_index == 0:
           s_first_dropdown.select_by_index(child_index + 1)
           continue
   return data_obj
# loop over case_type options and store data in
# dataArray
def loop_over_case_type_options(data_array):
   fill_search_year_input()
   case_type_dropdown = driver.find_element_by_id('case_type')
   case_type_options = case_type_dropdown.find_elements_by_xpath(".//*")
   for option_index in range(len(case_type_options)):
       # skip default option
       if option_index == 0:
           continue
       s_first_dropdown = Select(case_type_dropdown)
       s_first_dropdown.select_by_index(option_index)
       data = {
           'val': case_type_options[option_index].get_attribute('value'),
           'type': case_type_options[option_index].text
       }
       data_array.append(data)
       try:
           table = WebDriverWait(driver, 15).until(
               expected_conditions.presence_of_element_located((By.XPATH, "//td[contains(@class, 'col-xs')]"))
           )
           loop_through_table(driver)
       except(TimeoutException) as py_ex:
           print(py_ex)
           continue

# get only the first url for testing purpose
urls = get_case_type_urls_from_csv()[2:4]
r = open_page_using_url(urls)
print(r)
