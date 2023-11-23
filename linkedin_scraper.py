from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
from random import randint

import pandas as pd
import numpy as np
import re
import os

driver = webdriver.Chrome(ChromeDriverManager().install())

KEYWORDS = "Graduate Data Analyst"
LOCATION = "London"

kw_url =  "%20".join(KEYWORDS.split(" "))
loc_url = "%20".join(LOCATION.split(" "))

url = "https://www.linkedin.com/jobs/search?keywords=" + kw_url + "&location=" + loc_url

wait = WebDriverWait(driver, 5)
driver.maximize_window()
driver.get(url)

# Cookie Banner Handler
wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@action-type='ACCEPT']")))
driver.find_element_by_xpath("//*[@action-type='ACCEPT']").click()

# Scrolls down page to load listings and clicks "See more jobs button when it appears."
pages = 2
while pages > 0:
    wait = WebDriverWait(driver, randint(20,50)/10)
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='See more jobs']")))
        driver.find_element_by_xpath("//*[@aria-label='See more jobs']").click()
        sleep(randint(20,50)/10)
    except Exception:
        pass
    driver.find_element_by_tag_name("body").send_keys(Keys.END)
    pages -= 1

# Once here, the fun begins!
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

jobs_df = pd.DataFrame()

listings = soup.find_all("div", {"class": "base-search-card__info"})

# Get info from listings
for l in listings:
    new_record = {}
    # Title
    try:
        title = l.find("h3", {"class": "base-search-card__title"})
        title_reformat = re.sub("[^!-~(),]+", " ", title.text).strip()
        new_record["title"] = title_reformat
    except AttributeError:
        new_record["title"] = np.NaN

    # Company
    try:
        company = l.find("a", {"class": "hidden-nested-link"})
        company_reformat = re.sub("[^!-~(),]+", " ", company.text).strip()
        new_record["company"] = company_reformat
    except AttributeError:
        new_record["company"] = np.NaN

    # Location
    try:
        location = l.find("span", {"class": "job-search-card__location"})
        location_reformat = re.sub("[^!-~(),]+", " ", location.text).strip()
        new_record["location"] = location_reformat
    except AttributeError:
        new_record["location"] = np.NaN

    # List Date
    try:
        list_date = l.find("time").get("datetime")
        new_record["list_date"] = list_date
    except AttributeError:
        new_record["list_date"] = np.NaN

    # Salary
    try:
        salary = l.find("span", {"class": "job-search-card__salary-info"})
        salary_reformat = re.sub("[^!-~()]+", " ", salary.text).strip()
        new_record["salary_low"] = float(salary_reformat.split(" - ")[0].replace(",", ""))
        new_record["salary_high"] = float(salary_reformat.split(" - ")[1].replace(",", ""))
    except AttributeError:
        new_record["salary_low"] = np.NaN
        new_record["salary_high"] = np.NaN
        pass

    jobs_df = pd.concat([jobs_df, pd.DataFrame([new_record])], ignore_index=True)
    
# jobs_df.to_csv("linkedin_data.csv")
display(jobs_df)