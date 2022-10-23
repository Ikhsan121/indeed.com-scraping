from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time,json, os



URL = 'https://id.indeed.com'
# Creating a webdriver instance
chrome_driver_path = Service("C:\Development\chromedriver")
driver = webdriver.Chrome(service=chrome_driver_path)
# This instance will be used to log into indeed


def open_page(query, loc):
    driver.get(URL)
    # fill the form for job_title and location
    job_title = driver.find_element(By.NAME, 'q')
    job_title.send_keys(query)
    location = driver.find_element(By.NAME, 'l')
    location.send_keys(loc)
    location.send_keys(Keys.ENTER)
    time.sleep(1)


def next_page(page):
    if page == 2:
        # page 2
        link_list = []
        links = driver.find_elements(By.CLASS_NAME, "css-ho7khd")
        for link in links:
            link_list.append(link)
        link_list[page-2].click() # == 0
        time.sleep(5)
    # page 3
    elif page == 3:
        link_list = []
        links = driver.find_elements(By.CLASS_NAME, "css-ho7khd")
        for link in links:
            link_list.append(link)
        link_list[page-2].click() # == 1
        time.sleep(5)
    elif page == 4:
    #page 4
        link_list = []
        links = driver.find_elements(By.CLASS_NAME, "css-ho7khd")
        for link in links:
            link_list.append(link)
        link_list[page - 2].click() # == 2
        time.sleep(5)
    else:
        #page 5
        link_list = []
        links = driver.find_elements(By.CLASS_NAME, "css-ho7khd")
        for link in links:
            link_list.append(link)
        link_list[2].click()
        time.sleep(5)

def get_all_items(query, loc, page):

    # retrieve the html data
    page_source = driver.page_source

    # soup the html
    soup = BeautifulSoup(page_source, 'html.parser')

    # scraping process
    contents = soup.find_all('table', 'jobCard_mainContent big6_visualChanges')
    jobs_list = []
    for item in contents:
        title = item.find('h2', 'jobTitle').text
        company = item.find('span', 'companyName')
        company_name = company.text
        try:
            company_link = URL + company.find('a')['href']
        except:
            company_link = "Link is not available"

        # sorting data
        data_dict = {
            'title': title,
            'company name': company_name,
            'link': company_link,
        }
        jobs_list.append(data_dict)

    # writing json file
    try:
        os.mkdir('json_result')
    except FileExistsError:
        pass
    with open(f'json_result/{query}_in_{loc}_page_{page}.json', 'w+') as json_data:
        json.dump(jobs_list, json_data)
    print('json created')
    return True

def run():
    query = input("enter your query: ")
    loc = input("enter your location: ")
    open_page(query, loc)
    page = 1
    items = get_all_items(query=query, loc=loc, page=page)
    if items:
        page = 2
        next_page(page=page)
        items = get_all_items(query=query, loc=loc, page=page)
        if items:
            page = 3
            next_page(page=page)
            items = get_all_items(query=query, loc=loc, page=page)
            if items:
                page = 4
                next_page(page=page)
                items = get_all_items(query=query, loc=loc, page=page)
                if items:
                    page = 5
                    next_page(page=page)
                    items = get_all_items(query=query, loc=loc, page=page)



if __name__ == "__main__":
    run()