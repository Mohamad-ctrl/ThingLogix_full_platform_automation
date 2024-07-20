import utils
import auth
import navigate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException


def change_lang(driver, lang):
    driver.find_element(By.ID, "agent-canned-messages-form-field").click()
    time.sleep(5)
    xpath = f"//mat-option[@ng-reflect-value='{lang}']"
    element = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    return element


def create_message(driver, caseName, lang, reply):
    # add new button
    logging.info("clicking the add new button")
    driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-canned-messages-landing/app-canned-messages-list/div[1]/div/button").click()
    logging.info("clicked the add new button")
    time.sleep(5)
    # filling the case name input
    driver.find_element(By.ID, "agent-canned-messages-input").send_keys(caseName)
    #filling the reply text area
    driver.find_element(By.ID, "agent-canned-messages-textarea").send_keys(reply)
    # choosing the lang
    change_lang_btn = change_lang(driver, lang)
    change_lang_btn.click()
    time.sleep(5)
    # Add button
    add_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="agent-canned-messages-button"][@type="submit"]'))
    )
    add_button.click()
    # Searching for the message to make sure that it was added
    time.sleep(10)
    driver.find_element(By.ID, "agent-canned-messages-search").send_keys(reply)
    time.sleep(5)
    replyFromWeb = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-canned-messages-landing/app-canned-messages-list/div[2]/table/tbody/tr/td[1]").text
    caseNameFromWeb = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-canned-messages-landing/app-canned-messages-list/div[2]/table/tbody/tr/td[2]").text

    compReply = reply == replyFromWeb
    compCaseName = caseName == caseNameFromWeb

    if compReply and compCaseName:
        logging.info("Creating a canned message test: Passed ")
        return {"Test Name": "Create A Canned Message", "Test Results": "Passed"}
    else:
        logging.info(f"Creating a canned message test: Failed ")
        return {"Test Name": "Create A Canned Message", "Test Results": "Failed"}

def del_message(driver, reply, caseName):
    try:
        logging.info("searching for the message")
        searchInput = driver.find_element(By.ID, "agent-canned-messages-search")
        searchInput.send_keys(Keys.CONTROL + "a")
        searchInput.send_keys(Keys.DELETE)
        searchInput.send_keys(reply)
        time.sleep(5)
        replyFromWeb = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-canned-messages-landing/app-canned-messages-list/div[2]/table/tbody/tr/td[1]").text
        caseNameFromWeb = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-canned-messages-landing/app-canned-messages-list/div[2]/table/tbody/tr/td[2]").text
        if reply == replyFromWeb and caseName == caseNameFromWeb:
            driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-canned-messages-landing/app-canned-messages-list/div[2]/table/tbody/tr/td[5]/button[2]").click()
            time.sleep(3)
            driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/mat-dialog-container/app-confirmation-dialog/div[3]/button[2]").click()
            logging.info("Clicked the delete button")
            time.sleep(5)
            logging.info("Validating that the message was deleted")
            return validate_message_del(driver, reply, caseName)
    except Exception as e:
        logging.info("Error while trying to delete a canned message")
        return {"Test Name": "Deleting Canned Message", "Test Results": "Failed", "Error": "Error while trying to implement the test"}
    
def validate_message_del(driver, reply, caseName):
    searchInput = driver.find_element(By.ID, "agent-canned-messages-search")
    searchInput.send_keys(Keys.CONTROL + "a")
    searchInput.send_keys(Keys.DELETE)
    searchInput.send_keys(reply)
    try:
        replyFromWeb = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-canned-messages-landing/app-canned-messages-list/div[2]/table/tbody/tr/td[1]").text
        caseNameFromWeb = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-canned-messages-landing/app-canned-messages-list/div[2]/table/tbody/tr/td[2]").text
        logging.info("Message was not deleted")
        return {"Test Name": "Deleting Canned Message", "Test Results": "Failed"}
    except Exception as e:
        logging.info("Message was deleted susussfully")
        return {"Test Name": "Deleting Canned Message", "Test Results": "Passed"}
    
    
def edit_message(driver, currentRely, currentCaseName, currentLang, newRely = " ", newCaseName = " ", newLang = " "):
    if newRely == " ":
        newRely = currentRely
    if newCaseName == " ":
        newCaseName = currentCaseName
    if newLang == " ":
        newLang == "en"
    searchInput = driver.find_element(By.ID, "agent-canned-messages-search")
    searchInput.send_keys(Keys.CONTROL + "a")
    searchInput.send_keys(Keys.DELETE)
    time.sleep(2)
    searchInput.send_keys(currentRely)
    time.sleep(5)
    if driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-canned-messages-landing/app-canned-messages-list/div[2]/table/tbody/tr/td[1]").text == currentRely and currentCaseName == driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-canned-messages-landing/app-canned-messages-list/div[2]/table/tbody/tr/td[2]").text:
        # Edit button
        driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-canned-messages-landing/app-canned-messages-list/div[2]/table/tbody/tr[1]/td[5]/button[1]").click()
        # filling the new case name input
        time.sleep(5)
        caseNameInput = driver.find_element(By.ID, "agent-canned-messages-input")
        replyInput = driver.find_element(By.ID, "agent-canned-messages-textarea")
        caseNameInput.send_keys(Keys.CONTROL + "a")
        caseNameInput.send_keys(Keys.DELETE)
        time.sleep(2)
        caseNameInput.send_keys(newCaseName)
        #filling the reply text area
        replyInput.send_keys(Keys.CONTROL + "a")
        replyInput.send_keys(Keys.DELETE)
        time.sleep(2)
        replyInput.send_keys(newRely)
        # choosing the lang
        change_lang_btn = change_lang(driver, "en")
        change_lang_btn.click()
        time.sleep(5)
        # Add button
        add_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="agent-canned-messages-button"][@type="submit"]'))
        )
        add_button.click()
        # Searching for the message to make sure that it was added
        time.sleep(10)
        searchInput.send_keys(Keys.CONTROL + "a")
        searchInput.send_keys(Keys.DELETE)
        searchInput.send_keys(newRely)
        if newRely == driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-canned-messages-landing/app-canned-messages-list/div[2]/table/tbody/tr/td[1]").text:
            logging.info("Message was edit successfully")
            return {"Test Name": "Edit Canned Message", "Test Results": "Passed"}
        else:
            logging.info("Something went wrong, message was not edited")
            return {"Test Name": "Edit Canned Message", "Test Results": "Failed", "Error": "Error while trying to implement the test"}
    else:
        logging.info("Message was not found")
        return {"Test Name": "Edit Canned Message", "Test Results": "Failed", "Error": "Message was not found"}
