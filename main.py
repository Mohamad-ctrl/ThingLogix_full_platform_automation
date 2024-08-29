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
import helpdeskTests
import cannedTests
import reportsTests
import liveChat


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')# Function to compare responses

# Initialize WebDriver
service = Service('C:/Users/Mohammad/.wdm/drivers/chromedriver/win64/127.0.6533.72/chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.maximize_window() 

# The website URL
chat_url = "https://dqt6e7ekz6j0s.cloudfront.net/"

# Open the website
driver.get(chat_url)


# Wait for the page to load and the chat button to be clickable
chat_button = WebDriverWait(driver, 30).until(  
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".chatbot-toggle-icon img.ng-star-inserted"))
)

# Click the chat button
chat_button.click()

# Add a short wait to ensure chat box is fully opened
time.sleep(5)


# Live Chat tests
# file_path = "C:\\Users\\Mohamad\\Desktop\\login_as_agent_error.png"
# awsLink = "https://thinglogixce-new.awsapps.com/auth/?client_id=e5d4030c01266747&redirect_uri=https%3A%2F%2Fthinglogixce-new.my.connect.aws%2Fauth%2Fcode%3Fdestination%3D%252Fccp-v2%252F&state=wMjrRvhUw2n3lAZL0s_Vjl14SyAZuCYdsWyRoV-nKLwTm61MLbfV4bZ67RtZ6A5ZDjWAS3jQy5bA_G1R_WMvnA"
# overall_result, result_file = liveChat.live_chat(driver, "Mohamad", "test@example.com", "02341823945", "rida@thinglogix.com", "123", "test-uat", "Test@123", awsLink, file_path, "Test Description")
# print(f"Overall Result: {overall_result}")
# print(f"Test results saved to: {result_file}")


# # Reports tests
# result_file = reportsTests.reports_tests(driver, "rida@thinglogix.com", "123", "test-uat", "Test@123", awsLink, "maria+uat@thinglogix.com", "MZ@12345", "3", "5", "3")
# print(f"Test results saved to: {result_file}")

# # Canned messages tests
# replyT = "Test Reply"
# caseNameT = "Test Case Name"
# newReplyT = "New test reply"
# newCaseNameT = "New case name"
# result_file = cannedTests.cannedMessages(driver, caseNameT, replyT, newReplyT, newCaseNameT)
# print(f"Test results saved to: {result_file}")

# # Helpdesk Tests
# result_file = helpdeskTests.helpDiskTests(driver)
# print(f"Test results saved to: {result_file}")

# Engagement tester

# Admin login
adminEmail = ""
adminPassword = ""

# Arguments for channels new mail
newMailTemplate = ""
newMailSender = ""
newMailListOrPromo = ""
# the following arguments are optional you can keep them as 'None' or give them a value
newMailEmail = None
newMailNameInList = None 
newMailSendTime = None
newMailStartDate = None
newMailStartTime = None
newMailEndDate = None
newMailEndTime = None

# Arguments for new whatsapp message test (Note that this test costs money therfore if you wish to not do it just leave all its value empty)
# if you want to run the test just make sure to fill all arguments that has the '*' next to them
newWhatsTemp = None # *
newWhatsListOrPromo = None # *
newWhatsNumber = None # *
newWhatsLinkSur = None
newWhatsSendTime = None
newWhatsNameInList = None
newWhatsStartDate = None
newWhatsStartTime = None
newWhatsEndDate = None
newWhatsEndTime = None

# Arguments for new whatsapp message test (Note that this test also costs money therefore you will also have the option to leave all values empty in which the test will not be running)
# if you want to run the test just make sure to fill all arguments that has the '*' next to them
newSmsTemp = None
newSmsListOrPromo = None
# please provide either a phone number or a name in the contact list for this test
newSmsPhoneNumber = None
newSmsNameInList = None
# optional arguments
newSmsSendTime = None
newSmsStartDate = None
newSmsStartTime = None
newSmsEndDate = None
newSmsEndTime = None

# Arguments for new contact test
newContactListName = ""
newContactCsvFile = ""
# optional argument
newContactDetails = None


# Arguments for new custom filed
createNewFiled_FiledName = ""
createNewFiled_Example = ""

# Arguments for new template test
templatName = ""
templatSubject = ""
# optional argument
templateDesc = None
template_Template = None

# Arguments for new survey test
surveyTitle = ""

engagement.run_tests(driver, adminEmail, adminPassword, newMailTemplate, newMailSender, newMailListOrPromo, newWhatsTemp,
                      newWhatsListOrPromo, newWhatsNumber, newSmsTemp, newSmsListOrPromo, newContactListName, newContactCsvFile,
                        templatName, templatSubject, createNewFiled_FiledName, createNewFiled_Example, surveyTitle, newMailEmail,
                          newMailNameInList, newMailSendTime, newMailStartDate, newMailStartTime, newMailEndDate, newMailEndTime,
                            newWhatsLinkSur, newWhatsSendTime, newWhatsNameInList, newWhatsStartDate, newWhatsStartTime, newWhatsEndDate,
                              newWhatsEndTime, newSmsPhoneNumber, newSmsNameInList, newSmsSendTime, newSmsStartDate, newSmsStartTime,
                                newSmsEndDate, newSmsEndTime, newContactDetails, templateDesc, template_Template)

    
time.sleep(3000)
driver.quit()
