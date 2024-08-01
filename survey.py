from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import openpyxl
import time
import pandas as pd
import logging
import os
import auth
import utils
import navigate

def create_new_survey(driver, surveyTitle):
    logging.info("Locating and clicking new template button")
    create_new_survey_btn = WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//button[contains(., ' + New Survey ')]"))
    )
    create_new_survey_btn.click()
    time.sleep(5)
    utils.send_input_key(driver, "title", surveyTitle)
    send_btn = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tl-ce-submit[type='submit']"))
    )
    send_btn.click()
    time.sleep(10)
    driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-survey/div[3]/input").send_keys(surveyTitle)
    time.sleep(5)
    try:
        driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-survey/div[3]/table/tbody/tr[1]/td[1]")
        logging.info("survey found, test passed")
        return {"Test Name": "Create New Survey", "Test Results": "Passed"}
    except Exception as e:
        logging.info("survey was not found test failed")
        return {"Test Name": "Create New Survey", "Test Results": "Failed"}
