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
import channels

def run_channels_tests(driver):
    auth.loginAsAdmin(driver, "maria+uat@thinglogix.com", "MZ@12345")
    time.sleep(20)
    navigate.go_to_channels(driver)
    time.sleep(15)
    # channels.send_new_mail(driver, " test ", " rida@thinglogix.com ", "list", None, " VJ-Test ", " Hourly ", "07/28/2024", "09:58 AM", "08/08/2024", "09:06 PM")
    # channels.send_new_Whatsapp(driver, " vw_aftersales_message ", "promotional", "+971561091235", " Testing ")
    channels.send_new_sms(driver, " Test240724 ", "promotional", "+971561091235")
    logging.info("Passed")
