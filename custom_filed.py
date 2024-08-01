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

def create_new_filed(driver, filedName, example):
    logging.info("Locating and clicking new custom filed button")
    new_custom_filed = WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//button[contains(., ' + New Custom Field ')]"))
    )
    new_custom_filed.click()
    time.sleep(10)
    utils.send_input_key(driver, "name", filedName)
    time.sleep(5)
    utils.send_input_key(driver, "example", example)
    send_btn = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tl-ce-submit[type='submit']"))
    )
    send_btn.click()
def check_filed(driver, filedName):
    logging.info("verifiying the field creation")
    driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-engagement-landing/app-custom-fields-list/div[2]/input").send_keys(filedName)
    try:
        name_from_web = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-engagement-landing/app-custom-fields-list/div[2]/table/tbody/tr[1]/td[1]")
        logging.info("field was found test passed")
        return {"Test Name": "Create New Field", "Test Results": "Passed"}
    except Exception as e:
        logging.info("filed was not found test failed")
        return {"Test Name": "Create New Field", "Test Results": "Failed"}
