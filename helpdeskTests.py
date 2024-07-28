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

def save_help_desk_tests_results(results, writer):
    df = pd.DataFrame(results)
    df.to_excel(writer, sheet_name='Helpdesk Results', index=False)

def helpDiskTests(driver):
    results = []
    ticketSub = "Test ticked 000111"
    ticketDes = "test desc"
    logging.info("Running the helpdesk tests")
    # auth.loginAsAdmin(driver, "maria+uat@thinglogix.com", "MZ@12345")
    # logging.info("Logged in as an admin")
    # time.sleep(10)
    logging.info("Going to the helpdesk section in the website")
    navigate.go_to_helpdesk(driver)
    time.sleep(10)
    logging.info("Switching to the chat bot tab")
    driver.switch_to.window(driver.window_handles[0])
    logging.info("running the creating ticket test")
    creating_ticket_res = helpdesk.create_ticket_through_chatbot(driver, "chat", ticketSub, ticketDes)
    results.append(creating_ticket_res)
    logging.info("creating ticket test is done")
    time.sleep(15)
    logging.info("validating the ticket creation")
    validating_ticket_creation = helpdesk.check_message_in_web(driver, ticketSub, ticketDes, "open")
    results.append(validating_ticket_creation)
    logging.info("validation finished")
    time.sleep(10)
    logging.info("Testing deleting ticket")
    del_res = helpdesk.del_msg(driver, ticketSub)
    results.append(del_res)
    logging.info("All tests are finshed")
    currentDate = datetime.now()
    
    # Format the date and time
    formatted_date_time = currentDate.strftime("%d-%m_%I.%M%p").lower()
    
    # Create the file name
    file_name = f'help_desk_tests_results_{formatted_date_time}.xlsx'
    
    # Get the directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full file path
    result_file = os.path.join(script_directory, file_name)
    
    with pd.ExcelWriter(result_file, mode='w', engine='openpyxl') as writer:
        save_help_desk_tests_results(results, writer)

    return result_file