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
import reports
import navigate
import canned_messages
import helpdesk

def send_new_mail(driver, templet, sender, promoOrList, email = None, nameInList = None, sendTime = None, startDate = None, startTime = None, endDate = None, endTime = None):
    # Clicking the new msg btn
    logging.info("Lockating and clicking the New Message button")
    send_new_mail_btn = WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//button[contains(., ' New Message ')]"))
    )
    send_new_mail_btn.click()
    time.sleep(10)
    # Templet dropdown
    logging.info("Clicking the template dropdown")
    utils.select_dropdown_option(driver, "template", templet)
    # sender dropdown
    utils.select_dropdown_option(driver, "sender", sender)
    # choosing promo or list
    utils.select_radio_button(driver, promoOrList)
    time.sleep(5)
    if promoOrList == "promotional":
        logging.info("selecting the promotional")
        email_input_xpath = "//textarea[@formcontrolname='emails']"
        email_input = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, email_input_xpath))
        )
        email_input.send_keys(email)
    elif promoOrList == "list":
        logging.info("selecting the list option")
        # driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/mat-dialog-container/app-email/form/div[2]/div[2]/div/div[2]").click()
        # selecting the choosn name in list
        utils.select_dropdown_option(driver, "list", nameInList)
        # selecting the time
        utils.select_dropdown_option(driver, "frequency", sendTime)
        if sendTime == " Once " or " Hourly ":
            # setting the start date
            utils.set_date(driver, "startDate", startDate)
            # setting the start time
            utils.set_time(driver, "startTime", startTime)
            if sendTime == " Hourly ":
                # setting the end date
                utils.set_date(driver, "endDate", endDate)
                # setting end time
                utils.set_time(driver, "endTime", endTime)
    # send_btn = WebDriverWait(driver, 30).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tl-ce-submit[type='submit']"))
    # )
    # send_btn.click()

def send_new_Whatsapp(driver, templet, promoOrList, phoneNumber, linkSur = None, sendTime = None, nameInList = None, startDate = None, startTime = None, endDate = None, endTime = None):
    logging.info("Lockating and clicking the New Message button")
    send_new_msg_btn = WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-engagement-landing/app-channels/div[2]/div/div[2]/button"))
    )
    send_new_msg_btn.click()
    # Templet dropdown
    logging.info("Clicking the template dropdown")
    utils.select_dropdown_option(driver, "template", templet)
    # choosing promo or list
    utils.select_radio_button(driver, promoOrList)
    if promoOrList == "promotional":
        logging.info("filling the whatsapp number field")
        phone_input_xpath = "//textarea[@formcontrolname='whatsappNumbers']"
        phone_input = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, phone_input_xpath))
        )
        phone_input.send_keys(phoneNumber)
    elif promoOrList == "list":
        logging.info("selecting the list option")
        # driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/mat-dialog-container/app-email/form/div[2]/div[2]/div/div[2]").click()
        # selecting the choosn name in list
        utils.select_dropdown_option(driver, "list", nameInList)
        # selecting the time
        utils.select_dropdown_option(driver, "frequency", sendTime)
        if sendTime == " Once " or " Hourly ":
            # setting the start date
            utils.set_date(driver, "startDate", startDate)
            # setting the start time
            utils.set_time(driver, "startTime", startTime)
            if sendTime == " Hourly ":
                # setting the end date
                utils.set_date(driver, "endDate", endDate)
                # setting end time
                utils.set_time(driver, "endTime", endTime)
    # send_btn = WebDriverWait(driver, 30).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tl-ce-submit[type='submit']"))
    # )
    # send_btn.click()
    
