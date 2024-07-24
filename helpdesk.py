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


def check_message_in_web(driver, ticketSub, ticketDesc, status):
    try:
        dropDownList = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-helpdesk-ticket-landing/app-helpdesk-tickets-list/div[1]/div[1]/mat-form-field/div")
        dropDownList.click()
        time.sleep(5)
        xpath = f"//mat-option[@ng-reflect-value='{status}']"
        option = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        option.click()
        time.sleep(10)
        search_bar = driver.find_element(By.ID, "helpdesk-tickets-search")
        search_bar.send_keys(ticketSub)
        logging.info("Wating for the search res...")
        time.sleep(20)
        try:
            logging.info("trying to capture the info..")
            # Trying to capture randowm data from the website to make sure its fully loaded
            temp = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-helpdesk-ticket-landing/app-helpdesk-tickets-list/div[2]/table/tbody/tr[1]/td[7]").text
        except Exception as e:
            logging.info("Error in capturing the ticket data from the web")
            return
        ticketSubFromWeb = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-helpdesk-ticket-landing/app-helpdesk-tickets-list/div[2]/table/tbody/tr[1]/td[2]")
        ticketIdFromWeb = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-helpdesk-ticket-landing/app-helpdesk-tickets-list/div[2]/table/tbody/tr[1]/td[1]").text
        compSub = ticketSub == ticketSubFromWeb.text
        time.sleep(10)
        if compSub:
            logging.info("why am I here ?")
            ticketSubFromWeb.click()
            time.sleep(10)
            ticketDescFromWeb = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-helpdesk-view-ticket/div/div[2]/div/mat-card/mat-card-content/div[2]/div[1]/mat-card/mat-card-content/div/div[2]/p").text
            compDesc = ticketDesc == ticketDescFromWeb
            if compDesc:
                logging.info(f"Ticket was found:\nTicket ID: {ticketIdFromWeb}\nTicket Subject: {ticketSubFromWeb}\nTicket Description: {ticketDescFromWeb}")
                return "Pass"
            else:
                logging.info("Desc Sec: Ticket was not found")
                return "Fail"
        else:
            logging.info("Sub Sec: Ticket was not found")
            return "Fail"
    except Exception as e:
        logging.info("website timed-out while searching for the ticket wating for the search second res...")
        navigate.go_to_helpdesk(driver)
        time.sleep(15)
        search_bar.send_keys(ticketSub)
        time.sleep(20)


def create_ticket_through_chatbot(driver, btnOrChat, subject, description):
    if btnOrChat == "button":
        try:
            # Wait until the chatbot container is visible and interact with it
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "chatbot-container"))
            )

            # Find the "Talk To Agent" button by its text
            talk_to_agent_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//button[contains(., 'Create Ticket')]"))
            )
            
            # Click the "Talk To Agent" button
            talk_to_agent_button.click()
            
            # Wait for the response after clicking the button
            time.sleep(10)
            latest_response = utils.get_latest_response(driver)
            logging.info(f"Latest response: {latest_response}")
            
            # Expected response after clicking the button
            expected_response = "Please enter ticket subject"
            if utils.compare_responses(expected_response, latest_response):
                result = "Pass"
            else:
                result = "Fail"
            agent_details = {"Test name": "Create ticket through chatbot", "Action": btnOrChat, "Test Result": result}
            return result, agent_details
        
        except Exception as e:
            logging.error(f"Error occurred while trying to click the 'Talk To Agent' button: {e}")
            return "Fail", {
                "Action": "Talk to Agent Button",
                "Expected Response": expected_response,
                "Actual Response": str(e),
                "Passed": False
            }
    else:
        utils.automate_registration(driver, "hi", "Mohamad", "test@example.com", "02341823945")
        time.sleep(5)
        q = {"Create a ticket", f"{subject}", f"{description}"}
        e = {"Please enter ticket subject", "Please enter the description", "Your ticket has been created successfully!"}
        utils.automate_chat_testing(driver, q, e)