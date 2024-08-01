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
import engagement

def create_new_contact_list(driver, firstName, fileL, details = None):
    try:
        # Clicking the new contact list button
        logging.info("Locating and clicking new contact list button")
        new_contact_list_btn = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(., ' + New Contact List ')]"))
        )
        new_contact_list_btn.click()
        logging.info("Clicked new contact list button")
        time.sleep(5)  # Wait for the dialog to open

        # Filling the name input
        logging.info(f"Sending input '{firstName}' to name field")
        utils.send_input_key(driver, "name", firstName)

        # Checking if the details isn't empty
        if details:
            logging.info(f"Sending input '{details}' to details field")
            utils.send_input_key(driver, "details", details)

        # Make sure that the file exists
        if not os.path.isfile(fileL):
            logging.error(f"File not found: {fileL}")
            return

        # Locating the send file button
        logging.info("Locating file input element")
        file_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file' and @accept='.csv']"))
        )
        file_input.send_keys(fileL)
        logging.info(f"File path sent to input: {fileL}")
        send_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
        send_btn.click()
        logging.info("button clicked")
        return {"Test Name": "Create new contact list", "Test Results": "Passed"}

    except Exception as e:
        logging.error(f"An error occurred in create_new_contact_list: {e}")
        driver.save_screenshot('create_new_contact_list_error.png')
        return {"Test Name": "Create new contact list", "Test Results": "Failed", "Error": e}
    
def search_for_contact_list(driver, listName = "Maria Contact List"):
    searchInput = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-engagement-landing/app-contacts-list/div[2]/input")
    searchInput.send_keys(listName)
    time.sleep(10)
    # wait to get the search results then trying to verify that the contact is there
    try:
        list_name_in_web = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-engagement-landing/app-contacts-list/div[2]/table/tbody/tr[1]/td[1]")
        logging.info(f"Found list: {list_name_in_web}")
        return {"Test Name": "Create new contact list", "Test Results": "Passed"}
    except Exception as e:
        logging.info(f"contact was not created test failed!")
        return {"Test Name": "Create new contact list", "Test Results": "Failed"}

    