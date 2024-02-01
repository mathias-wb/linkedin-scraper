from bs4 import BeautifulSoup
from random import randint
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager

import numpy as np
import pandas as pd


import re
import os

driver = webdriver.Chrome(ChromeDriverManager().install())

KEYWORDS = "Graduate Data Analyst -Business -Engineer -Scientist"
LOCATION = "London"
PAGES = 5

kw_url =  "%20".join(KEYWORDS.split(" "))
loc_url = "%20".join(LOCATION.split(" "))

url = "https://www.linkedin.com/jobs/search?keywords=" + kw_url + "&location=" + loc_url

wait = WebDriverWait(driver, 5)
driver.get(url)

# Cookie Banner Handler
wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@action-type='ACCEPT']")))
driver.find_element_by_xpath("//*[@action-type='ACCEPT']").click()


# Scrolls down page to load listings and clicks "See more jobs button when it appears."
pages_viewed = 0
while pages_viewed < PAGES:
    
    sleep(randint(10,20)/10)
    try:
        driver.find_element(By.XPATH, "//*[@class='px-1.5 flex inline-notification text-color-signal-positive see-more-jobs__viewed-all']")
        print("No more available listings!")
        break
    except exceptions.NoSuchElementException:
        pass

    try:
        driver.find_element_by_xpath("//*[@aria-label='See more jobs']").click()
        print("Loading more jobs...")
    except exceptions.ElementNotInteractableException:
        pass

    pages_viewed += 1
    print(f"{pages_viewed}/{PAGES} pages viewed.")

    
    driver.find_element_by_tag_name("body").send_keys(Keys.END)


# Once here, the fun begins!
html = driver.page_source
driver.close()

soup = BeautifulSoup(html, "html.parser")

jobs_df = pd.DataFrame()

listings = soup.find_all("div", {"class": "base-search-card__info"})

# Get info from listings
for l in listings:
    new_record = {}
    # Title
    try:
        title = l.find("h3", {"class": "base-search-card__title"})
        title_reformat = title.text.strip()
        new_record["title"] = title_reformat
    except AttributeError:
        new_record["title"] = np.NaN

    # Company
    try:
        company = l.find("a", {"class": "hidden-nested-link"})
        new_record["company"] = company.text.strip()
    except AttributeError:
        new_record["company"] = np.NaN

    # Location
    try:
        location = l.find("span", {"class": "job-search-card__location"})
        new_record["location"] = location.text.strip()
    except AttributeError:
        new_record["location"] = np.NaN

    # List Date
    try:
        list_date = l.find("time")
        new_record["list_date"] = list_date.get("datetime")
    except AttributeError:
        new_record["list_date"] = np.NaN

    # Salary
    try:
        salary = l.find("span", {"class": "job-search-card__salary-info"})
        salary = salary.text.strip()
        new_record["salary_low"] = float(salary.split(" - ")[0].replace(",", "")[1:])
        new_record["salary_high"] = float(salary.split(" - ")[1].replace(",", "")[1:])
    except AttributeError:
        new_record["salary_low"] = np.NaN
        new_record["salary_high"] = np.NaN
        pass

    jobs_df = pd.concat([jobs_df, pd.DataFrame([new_record])], ignore_index=True)
    
# jobs_df.to_csv("linkedin_data.csv",index=False)
jobs_df["list_date"] = pd.to_datetime(jobs_df["list_date"])
jobs_df.sort_values(by="list_date", ascending=False)
display(jobs_df)