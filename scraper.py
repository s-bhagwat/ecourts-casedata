from selenium import webdriver
from selenium.webdriver.support.ui import Select
from csv_reader import get_urls

COURT_TYPE_COMPLEX = 0
COURT_TYPE_ESTABLISHMENT = 1


def get_all_types(driver, court_type):
    d = {}
    fd = None
    sd = driver.find_element_by_id('case_type')

    if court_type == COURT_TYPE_COMPLEX:
        fd = driver.find_element_by_id('court_complex_code')
    else:
        fd = driver.find_element_by_id('court_code')

    ch = fd.find_elements_by_xpath(".//*")

    for x in range(1, len(ch)):
        s_first_dropdown = Select(fd)
        s_first_dropdown.select_by_index(x)
        first_dropdown_name = s_first_dropdown.first_selected_option.text

        d[first_dropdown_name] = []
        second_dropdown_children = sd.find_elements_by_xpath(".//*")

        for y in range(len(second_dropdown_children)):
            if y == 0:
                continue

            type_d = {
                'val': second_dropdown_children[y].get_attribute('value'),
                'type': second_dropdown_children[y].text
            }

            d[first_dropdown_name].append(type_d)

        if x == 0:
            s_first_dropdown.select_by_index(x + 1)
            continue

    return d


def run_get_all_types(data):
    driver = webdriver.Firefox('./geckodriver')

    for block in data:
        driver.get(block['url'])

        block['courtComplex'] = get_all_types(driver, COURT_TYPE_COMPLEX)
        driver.find_element_by_id('radCourtEst').click()
        block['courtEstablishment'] = get_all_types(driver, COURT_TYPE_ESTABLISHMENT)

    return data


urls = get_urls()[:1]
r = run_get_all_types(urls)
print(r)
