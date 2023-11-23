from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
from random import randint

import re

driver = webdriver.Chrome(ChromeDriverManager().install())

KEYWORDS = "Product Designer"
LOCATION = "London"

kw_url =  "%20".join(KEYWORDS.split(" "))
loc_url = "%20".join(LOCATION.split(" "))

url = "https://www.linkedin.com/jobs/search?keywords=" + kw_url + "&location=" + loc_url


wait = WebDriverWait(driver, 5)
driver.get(url)

# Cookie Handler
wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@action-type='ACCEPT']")))
driver.find_element_by_xpath("//*[@action-type='ACCEPT']").click()

# Scroll down page to load listings
for _ in range(6):
    driver.find_element_by_tag_name("body").send_keys(Keys.END)
    sleep(randint(20, 50)/10)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

listings = soup.find_all("a", {"data-tracking-control-name": "public_jobs_jserp-result_search-card"})

# Get listing titles
for l in listings:
    try:
        title = l.find("span", {"class": "sr-only"})
        title_reformat = re.sub("[^!-~()]+", " ", title.text).strip()
        print(title_reformat)
    except AttributeError:
        pass
    # TODO click "See more jobs" button when listings stop loading