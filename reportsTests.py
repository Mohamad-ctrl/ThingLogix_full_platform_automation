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

def save_report_results(results, writer):
    df = pd.DataFrame(results)
    df.to_excel(writer, sheet_name='Report Results', index=False)

def reports_tests(driver, uatAgentEmail, uatAgentPassword, awsUsername, awsPassword, awsLink, adminEmail, adminPassword, firstRate, secondRate, thirdRate):
    results = []
    
    # Validate Survey Test
    survey_result = reports.validate_survey(driver, adminEmail, adminPassword, firstRate, secondRate, thirdRate)
    results.append(survey_result)
    time.sleep(10)
    
    # Validate User Management Test
    um_result = reports.validate_UM(driver)
    results.append(um_result)
    
    # Save results to an Excel file
    # Generate the current date and time
    currentDate = datetime.now()
    
    # Format the date and time
    formatted_date_time = currentDate.strftime("%d-%m_%I.%M%p").lower()
    
    # Create the file name
    file_name = f'report_test_results_{formatted_date_time}.xlsx'
    
    # Get the directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full file path
    result_file = os.path.join(script_directory, file_name)
    
    with pd.ExcelWriter(result_file, mode='w', engine='openpyxl') as writer:
        save_report_results(results, writer)
    
    return result_file
