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

def send_keys_to_editor(driver, text):
    # Locate the contenteditable div using its class or other attributes
    editor = driver.find_element(By.CSS_SELECTOR, 'div.angular-editor-textarea[contenteditable="true"]')

    # Clear any existing content (optional)
    editor.clear()

    # Send the desired text to the editor
    editor.send_keys(text)

def create_new_template(driver, name, subject, description = None, template = None):
    logging.info("Locating and clicking new template button")
    create_new_template = WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//button[contains(., ' + New Template ')]"))
    )
    create_new_template.click()
    time.sleep(5)
    utils.send_input_key(driver, "name", name)
    time.sleep(3)
    utils.send_input_key(driver, "subject", subject)
    time.sleep(3)
    if description != None:
        utils.send_input_key(driver, "description", description)
    if template != None:
        send_keys_to_editor(driver, template)
    send_btn = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tl-ce-submit[type='submit']"))
    )
    send_btn.click()

def check_template(driver, templateName):
    driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-engagement-landing/app-template-list/div[2]/input").send_keys(templateName)
    try:
        driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-engagement-landing/app-template-list/div[2]/table/tbody/tr[1]/td[1]")
        logging.info("Template was found, test passed")
        return {"Test Name": "Create new template", "Test Results": "Passed"}
    except Exception as e:
        logging.info("Test failed template was not found")
        return {"Test Name": "Create new template", "Test Results": "Failed"}


