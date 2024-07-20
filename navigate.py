from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
import os


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
download_dir = "C:\\Users\\Mohamad\\Downloads"

def go_to_reports(driver, section = "defult"):
    try:
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://uat.thinglogixce.app/home/chats/agent/reports")
        logging.info("Opened the reports page")
        time.sleep(15)
        if section == "User Management":
            logging.info("Trying to click the change section button")
            changeSectionBTN = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-reports-landing/div/div/mat-form-field/div/div[1]'))
            )
            changeSectionBTN.click()
            logging.info("clicked the change section button")
            UserMangBTN = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[2]/div/div/div/mat-option[2]'))
            )
            UserMangBTN.click()
            return "Passed"
        elif section == "Survey":
            changeSectionBTN = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-reports-landing/div/div/mat-form-field/div/div[1]'))
            )
            changeSectionBTN.click()
            SurveyBTN = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[2]/div/div/div/mat-option[5]'))
            )
            SurveyBTN.click()
            return "Passed"
    except Exception as e:
        logging.error(f"Error while navigateing to reports: {e}", exc_info=True)
        return "Fail"
    
# Function to monitor the directory for new files and return the latest one
def wait_for_latest_download(download_dir, timeout=30):
    start_time = time.time()
    latest_file = None
    latest_time = 0
    while True:
        files = os.listdir(download_dir)
        for file in files:
            file_path = os.path.join(download_dir, file)
            file_time = os.path.getctime(file_path)
            if file_time > latest_time:
                latest_time = file_time
                latest_file = file_path
        
        if latest_file and time.time() - latest_time > 2:
            return latest_file  # Return the most recently added file
        
        if time.time() - start_time > timeout:
            break
        time.sleep(1)
    return None

def export_csv_reports(driver):
    try:
        exportButton = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-reports-landing/div/div/app-report-filters/div/button'))
        )
        exportButton.click()
        time.sleep(5)
        # Wait for the download to complete
        downloaded_file = wait_for_latest_download(download_dir)
        if downloaded_file:
            file_name, file_extension = os.path.splitext(downloaded_file)
            print(f"Downloaded file: {downloaded_file}")
            print(f"File name: {file_name}")
            print(f"File type: {file_extension}")
            return "Pass"
        else:
            logging.info("File download timed out or failed.")
            return "Fail"
    except Exception as e:
        logging.info(f"Error in exporting the csv file: {e}")
        return "Fail"

def go_to_canned_messages(driver):
    logging.info("going to the canned messages page")
    driver.get("https://uat.thinglogixce.app/home/chats/agent/canned-messages/list")