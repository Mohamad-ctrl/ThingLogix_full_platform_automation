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
import contacts
import custom_filed
import templates
import survey

def save_channels_results(results, writer):
    df = pd.DataFrame(results)
    df.to_excel(writer, sheet_name='Channels Results', index=False)

def save_other_tests(results, writer):
    df = pd.DataFrame(results)
    df.to_excel(writer, sheet_name='Other tests', index=False)



def run_tests(driver, adminEmail, adminPassword, newMailTemp, newMailSender, newMailListOrPromo, newWhatsTemp, newWhatsListOrPromo, newWhatsNumber, newSmsTemp, newSmsListOrPromo, newContactListName, newContactCsvFile, templateName, templateSubject, createNewFiled_FiledName, createNewFiled_Example, survetTitle, newMailEmail = None, newMailNameInList = None, newMailSendTime = None, newMailStartDate = None, newMailStartTime = None, newMailEndDate = None, newMailEndTime = None, newWhatsLinkSur = None, newWhatsSendTime = None, newWhatsNameInList = None, newWhatsStartDate = None, newWhatsStartTime = None, newWhatsEndDate = None, newWhatsEndTime = None, newSmsPhoneNumber = None, newSmsNameInList = None, newSmsSendTime = None, newSmsStartDate = None, newSmsStartTime = None, newSmsEndDate = None, newSmsEndTime = None, newContactDetails = None, templateDesc = None, template_Template = None):
    other_tests_results = []
    channels_results = []
    auth.loginAsAdmin(driver, adminEmail, adminPassword)
    time.sleep(20)
    navigate.go_to_channels(driver)
    time.sleep(15)
    new_mail_test_res = channels.send_new_mail(driver, newMailTemp, newMailSender, newMailListOrPromo, newMailEmail, newMailNameInList, newMailSendTime, newMailStartDate, newMailStartTime, newMailEndDate, newMailEndTime)
    channels_results.append(new_mail_test_res)
    time.sleep(10)
    navigate.go_to_channels(driver)
    time.sleep(15)
    new_whatsapp_tests_res = channels.send_new_Whatsapp(driver, newWhatsTemp, newWhatsListOrPromo, newWhatsNumber, newWhatsLinkSur, newWhatsSendTime, newWhatsNameInList, newWhatsStartDate, newWhatsStartTime, newWhatsEndDate, newWhatsEndTime)
    channels_results.append(new_whatsapp_tests_res)
    time.sleep(10)
    navigate.go_to_channels(driver)
    time.sleep(15)
    new_sms_tests_res = channels.send_new_sms(driver, newSmsTemp, newSmsListOrPromo, newSmsPhoneNumber, newSmsNameInList, newSmsSendTime, newSmsStartDate, newSmsStartTime, newSmsEndDate, newSmsEndTime)
    channels_results.append(new_sms_tests_res)
    time.sleep(10)
    contacts.create_new_contact_list(driver, newContactListName, newContactCsvFile, newContactDetails)
    time.sleep(10)
    create_new_contact_res = contacts.search_for_contact_list(newContactListName)
    other_tests_results.append(create_new_contact_res)
    time.sleep(5)
    navigate.go_to_custom_filed(driver)
    time.sleep(15)
    custom_filed.create_new_filed(driver, createNewFiled_FiledName, createNewFiled_Example)
    time.sleep(10)
    custom_filed_test_res = custom_filed.check_filed(driver, createNewFiled_FiledName)
    other_tests_results.append(custom_filed_test_res)
    time.sleep(5)
    navigate.go_to_templates(driver)
    time.sleep(15)
    templates.create_new_template(driver, templateName, templateSubject, templateDesc, template_Template)
    time.sleep(5)
    tempRes = templates.check_template(driver, templateName)
    other_tests_results.append(tempRes)
    time.sleep(5)
    navigate.go_to_survey(driver)
    surRes = survey.create_new_survey(driver, survetTitle)
    other_tests_results.append(surRes)
    logging.info("tests are finished")
    currentDate = datetime.now()
    # Format the date and time
    formatted_date_time = currentDate.strftime("%d-%m_%I.%M%p").lower()
    
    # Create the file name
    file_name = f'engagement_tests_results_{formatted_date_time}.xlsx'
    
    # Get the directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full file path
    result_file = os.path.join(script_directory, file_name)
    
    with pd.ExcelWriter(result_file, mode='w', engine='openpyxl') as writer:
        save_channels_results(channels_results, writer)
        save_other_tests(other_tests_results, writer)

    return result_file

def test(driver):
    auth.loginAsAdmin(driver, "maria+uat@thinglogix.com", "MZ@12345")
    time.sleep(20)
    navigate.go_to_contacts(driver)
    time.sleep(15)
    fileL = "C:\\Users\\Mohammad\\Downloads\\contactListExample.csv"
    contacts.create_new_contact_list(driver, "Mohamad Test", fileL, "test details")
