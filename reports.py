import navigate
import auth
import utils
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ending of this: loged in as admin in uat page: 1
def validate_survey(driver, adminEmail, adminPassword, firstRating, secondRating, thirdRating):
    # utils.automate_registration(driver, "hi", "Mohamad", "test@example.com", "02341823945")
    # utils.talkToAgent(driver, "button")
    # driver.switch_to.window(driver.window_handles[1])
    # time.sleep(10)
    # utils.acceptOrReject(driver, "accept")
    # time.sleep(10)
    # utils.end_agent_chat(driver)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
    # auth.rateAgent(driver)
    q = [f"Rate our agent", {firstRating}, {secondRating}, {thirdRating}]
    e = ["It would be great to rate our services using the scale below.Please select one of the following:", "Did you find it easy to contact us?Please select one of the following:", "Thank you for your time and your rating. Looking to serve you again!", "I would appreciate it if you could take a few moments to fill out a quick survey about my service. How would you rate the performance of the customer service employee who served you?Please select one of the following:"]
    utils.automate_chat_testing(driver, q, e)
    time.sleep(10)
    driver.switch_to.window(driver.window_handles[1])
    utils.logout(driver)
    time.sleep(10)
    auth.loginAsAdmin(driver, adminEmail, adminPassword)
    time.sleep(20)
    navigate.go_to_reports(driver, "Survey")
    time.sleep(15)
    firstRatingFromWeb = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-reports-landing/app-survey/div/table/tbody/tr[1]/td[4]").text
    secondRatingFromWeb = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-reports-landing/app-survey/div/table/tbody/tr[1]/td[5]").text
    thirdRatingFromWeb = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-reports-landing/app-survey/div/table/tbody/tr[1]/td[6]").text
    
    compareFirstRating = firstRating == firstRatingFromWeb
    compareSecondRating = secondRating == secondRatingFromWeb
    compareThirdRating = thirdRating == thirdRatingFromWeb

    logging.info(f"First rating: {firstRating}, Second rating: {secondRating}, Third rating: {thirdRating}")
    logging.info(f"First rating from web: {firstRatingFromWeb}, Second rating from web: {secondRatingFromWeb}, Third rating from web: {thirdRatingFromWeb}")

    if compareFirstRating and compareSecondRating and compareThirdRating:
        logging.info("All ratings matches. Test passed")
        details = {"Test Name": "Survey", "Rate Given To Agent": f"{firstRating}, {secondRating}, {thirdRating}", "Rate Written In The Platform": f"{firstRatingFromWeb}, {secondRatingFromWeb}, {thirdRatingFromWeb}", "Test Result": "Passed"}
        return details
    else:
        details = {"Test Name": "Survey", "Rate Given To Agent": f"{firstRating}, {secondRating}, {thirdRating}", "Rate Written In The Platform": f"{firstRatingFromWeb}, {secondRatingFromWeb}, {thirdRatingFromWeb}", "Test Result": "Failed"}
        logging.info("Test failed")
        return details
    
def validate_UM(driver):
    navigate.go_to_reports(driver, "User Management")
    time.sleep(15)
    test_res = navigate.export_csv_reports(driver)
    if test_res == "Pass":
        return {"Test Name": "User Mangement Export Test", "Test Result": "Passed"}
    else:
        return {"Test Name": "User Mangement Export Test", "Test Result": "Failed"}