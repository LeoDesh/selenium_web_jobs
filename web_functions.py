from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import date

import time


def karriere_df(
    job_field: str, location: str, waiting_seconds: float, filename: str = ""
):
    link = "https://www.karriere.at/jobs/[JOB_FIELD]/[LOCATION]"
    link = link.replace("[JOB_FIELD]", job_field.replace(" ", "-"))
    link = link.replace("[LOCATION]", location)
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(link)
    # driver.implicitly_wait(10.0)
    count = 0
    choice = True

    while choice:
        try:
            lenOfPage = driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"
            )
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "onetrust-reject-all-handler"))
            ).click()
            choice = False
        except:
            count = count + 1
            choice = False
            print("Attempt: " + str(count))
            pass

    driver.implicitly_wait(waiting_seconds)
    ##div.c-jobsSearch__jobsSearchList > div.m-jobsSearchList > div.m-jobsSearchList__loadMoreJobsButton > nav > button
    continue_button = "div.c-jobsSearch__jobsSearchList > div.m-jobsSearchList > div.m-jobsSearchList__loadMoreJobsButton > nav > button"
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"
    )

    match = False
    while not match:
        lastCount = lenOfPage
        time.sleep(1.0)
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"
        )
        if lastCount == lenOfPage:
            try:
                driver.find_element(By.CSS_SELECTOR, continue_button).click()
            except:
                match = True
    time.sleep(waiting_seconds)
    jobs = driver.find_elements(By.CSS_SELECTOR, "li.m-jobsList__item")
    data = []
    count = 0
    cols = ["Title", "JobLink", "Company", "Location"]
    element = driver.find_element(
        By.CSS_SELECTOR,
        "div.c-jobsSearch__listing > div.c-jobsSearch__jobsSearchList > div.m-jobsSearchList > div.m-jobsSearchList__header > div > div > h1 > span",
    )
    job_amount = int(element.text.split(" ")[0])
    for index, job in enumerate(jobs):
        try:
            title = job.find_element(
                By.CSS_SELECTOR, "div.m-jobsListItem__dataContainer > h2 > a"
            )

            job_link = job.find_element(
                By.CSS_SELECTOR, "div.m-jobsListItem__dataContainer > h2 > a"
            ).get_attribute("href")

            company = job.find_element(
                By.CSS_SELECTOR,
                "div.m-jobsListItem__dataContainer > div.m-jobsListItem__company > a",
            )

            try:
                """ location = job.find_element(
                    By.CSS_SELECTOR, "div.m-jobsListItem__wrap > ul > li > a"
                ) 
                location = job.find_element(
                    By.CSS_SELECTOR, "span.m-jobsListItem__locations m-jobsListItem__pill > a"   
                )
                """  # span.m-jobsListItem__locations m-jobsListItem__pill // should be > // span.m-jobsListItem__locations.m-jobsListItem__pill
                location = job.find_element(
                    By.CSS_SELECTOR, "div.m-jobsListItem__pills > span > a"
                )
            except:  # span.m-jobsListItem__location
                location = job.find_element(
                    By.CSS_SELECTOR,
                    "div.m-jobsListItem__pills > span > span",  # span.m-jobsListItem__location
                )

                """ location = job.find_element(
                    By.CSS_SELECTOR, "div.m-jobsListItem__wrap > ul > li > span"
                ) """
            data.append([title.text, job_link, company.text, location.text])
            # print([title.text,job_link,company.text,location.text])

            # print("Job: " + title.text + " at the company: " + company.text + " in: " + location.text + " with the following Job-Link: " + job_link)
        except (NoSuchElementException, StaleElementReferenceException):
            pass

    driver.quit()
    df_data = pd.DataFrame(data, columns=cols)
    if filename:
        df_data.to_csv(filename, index=False, mode="a")
    else:
        print(df_data)


def ams_df(job_field: str, location: str, waiting_seconds: float, filename: str = ""):
    delimiter = "%20"
    ams_link = "https://jobs.ams.at/public/emps/jobs?page=1&query=[JOB]&location=[LOCATION]&JOB_OFFER_TYPE=SB_WKO&JOB_OFFER_TYPE=IJ&JOB_OFFER_TYPE=BA&PERIOD=ALL&sortField=_SCORE"
    ams_link = ams_link.replace("[JOB]", job_field.replace(" ", delimiter))
    ams_link = ams_link.replace("[LOCATION]", location)
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(ams_link)
    driver.implicitly_wait(waiting_seconds)
    button = driver.find_element(By.CSS_SELECTOR, "div.container")
    div_part = "div.col-sm-6 col-lg-12 col-xl-auto".replace(" ", ".")
    button.find_element(By.CSS_SELECTOR, div_part + " > button").click()

    """  education_id = "ams-search-filter-selection-filter-3-header-text"
    element = driver.find_element(By.ID, education_id)
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].click();", element)

    education_input_id = "ams-search-filter-selection-filter-3-options-U*"
    element = driver.find_element(By.ID, education_input_id)
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].click();", element) """

    # time.sleep(waiting_seconds)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    # job_str = "ams-search-result-text"
    # job_amount = int(driver.find_element(By.ID,job_str).text.split(" ")[0])
    # print(job_amount)
    current_url = driver.current_url
    choice = True
    button_location = "ams-search-list-next-link"
    data = []
    cols = ["Title", "JobLink", "Company", "Location"]
    while choice:
        time.sleep(waiting_seconds)
        jobs_all = driver.find_element(By.ID, "ams-search-result-list")
        jobs = jobs_all.find_elements(By.CSS_SELECTOR, "sn-list-item-container")
        for job in jobs:
            try:
                job_title = job.find_element(
                    By.CSS_SELECTOR, "sn-list-item-header > h2 > a"
                ).text
                job_link = job.find_element(
                    By.CSS_SELECTOR, "sn-list-item-header > h2 > a"
                ).get_attribute("href")
                job_location = job.find_element(
                    By.ID, "ams-search-joboffer-location"
                ).text
                job_company = job.find_element(
                    By.ID, "ams-search-joboffer-company"
                ).text

                data.append([job_title, job_link, job_location, job_company])
            except (NoSuchElementException, StaleElementReferenceException):
                # print("Checking...")
                pass

        # time.sleep(2.5)
        element = driver.find_element(By.ID, button_location)
        driver.execute_script("arguments[0].scrollIntoView();", element)
        driver.execute_script("arguments[0].click();", element)
        if driver.current_url == current_url:
            time.sleep(waiting_seconds)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"
            )
            # job_str = "ams-search-result-text"
            # job_amount = int(driver.find_element(By.ID, job_str).text.split(" ")[0])
            choice = False
        else:
            current_url = driver.current_url

    driver.quit()
    df_data = pd.DataFrame(data, columns=cols)
    if filename:
        df_data.to_csv(filename, index=False, mode="a")
    else:
        print(df_data)
