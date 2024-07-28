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
import engagement

def save_canned_megs_results(results, writer):
    df = pd.DataFrame(results)
    df.to_excel(writer, sheet_name='Canned Messages Results', index=False)

def cannedMessages(driver, caseName, reply, newReply, newCaseName, adminEmail, adminPassword):
    results = []
    # logging.info("Logging in as admin")
    # auth.loginAsAdmin(driver, adminEmail, adminPassword)
    # time.sleep(15)
    navigate.go_to_canned_messages(driver)
    time.sleep(15)
    logging.info("Creating a canned message")
    creat_msg_test = canned_messages.create_message(driver, caseName, "en", reply)
    results.append(creat_msg_test)
    time.sleep(10)
    logging.info("Editing a canned message")
    edit_msg_test = canned_messages.edit_message(driver, reply, caseName, "en", newReply, newCaseName)
    results.append(edit_msg_test)
    time.sleep(5)
    logging.info("Deleting a canned message")
    del_msg_test = canned_messages.del_message(driver, newReply, newCaseName)
    results.append(del_msg_test)
    logging.info("Finished the canned messages tests")
    currentDate = datetime.now()
    # Format the date and time
    formatted_date_time = currentDate.strftime("%d-%m_%I.%M%p").lower()
    
    # Create the file name
    file_name = f'canned_messages_test_results_{formatted_date_time}.xlsx'
    
    # Get the directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full file path
    result_file = os.path.join(script_directory, file_name)
    
    with pd.ExcelWriter(result_file, mode='w', engine='openpyxl') as writer:
        save_canned_megs_results(results, writer)

    return result_file