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
    # try:
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)
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
    ticketSubFromWeb = driver.find_element(By.CLASS_NAME, "mat-cell.cdk-cell.tl-ce-clickable.tl-ce-wrap-content.cdk-column-a-title.mat-column-a-title.ng-star-inserted")
    ticketSubFromWebAsText = ticketSubFromWeb.text
    ticketIdFromWeb = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-helpdesk-ticket-landing/app-helpdesk-tickets-list/div[2]/table/tbody/tr[1]/td[1]").text
    compSub = ticketSub == ticketSubFromWeb.text
    time.sleep(10)
    if compSub:
        ticketSubFromWeb.click()
        time.sleep(10)
        ticketDescFromWeb = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-helpdesk-view-ticket/div/div[2]/div/mat-card/mat-card-content/div[2]/div[1]/mat-card/mat-card-content/div/div[2]/p").text
        compDesc = ticketDesc == ticketDescFromWeb
        if compDesc:
            logging.info(f"Ticket was found:\nTicket ID: {ticketIdFromWeb}\nTicket Subject: {ticketSubFromWebAsText}\nTicket Description: {ticketDescFromWeb}")
            return {
                "Test Name": "Valitating the created ticket",
                "Original Ticket Details": f"Ticket Subject: {ticketSub}, Ticket Description: {ticketDesc}",
                "Ticket Details Found In Web": f"Ticket ID: {ticketIdFromWeb}, Ticket Subject: {ticketSub}, Ticket Descrption: {ticketDesc}",
                "Test Results": "Passed"
            }
        else:
            logging.info("Desc Sec: Ticket was not found")
            return {
                "Test Name": "Valitating the created ticket",
                "Original Ticket Details": f"Ticket Subject: {ticketSub}, Ticket Description: {ticketDesc}",
                "Ticket Details Found In Web": f"Ticket ID: {ticketIdFromWeb}, Ticket Subject: {ticketSub}, Ticket Descrption: {ticketDesc}",
                "Test Results": "Failed",
                "Error": str(e)
            }
    else:
        logging.info("Sub Sec: Ticket was not found")
        return {
                "Test Name": "Valitating the created ticket",
                "Original Ticket Details": f"Ticket Subject: {ticketSub}, Ticket Description: {ticketDesc}",
                "Ticket Details Found In Web": f"Ticket ID: {ticketIdFromWeb}, Ticket Subject: {ticketSub}, Ticket Descrption: {ticketDesc}",
                "Test Results": "Failed",
                "Error": str(e)
            }
    # except Exception as e:
    #     logging.info("website timed-out while searching for the ticket hang tied while I try the test again")
    #     navigate.go_to_helpdesk(driver)
    #     time.sleep(10)
    #     check_message_in_web(driver, ticketSub, ticketDesc, status)
    


def create_ticket_through_chatbot(driver, btnOrChat, subject, description):
    if btnOrChat == "button":
        logging.info("Sending the messages by Button")
        try:
            # Wait until the chatbot container is visible and interact with it
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "chatbot-container"))
            )

            utils.automate_registration(driver, "hi", "Mohamad", "test@example.com", "02341823945")

            time.sleep(10)
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
            return {
                "Test Name": "Create ticket through chatbot",
                "Action": f"Talk to Agent Button",
                "Test Results": "Failed",
                "Error": str(e)
            }
    else:
        logging.info("Sending the messages by chat")
        time.sleep(5)
        q = ["Create a ticket", f"{subject}", f"{description}"]
        logging.info(f"questions: {q}")
        e = ["Please enter ticket subject", "Please enter the description", "Your ticket has been created successfully!"]
        utils.automate_chat_testing(driver, q, e)
        return {
            "Test Name": "Create ticket through chatbot",
            "Action": "Talk to Agent Chat",
            "Test Results": "Passed"
        }

def del_msg(driver, ticket_sub):
    logging.info(f"Deleting the following message : {ticket_sub}")
    try:
        driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-chats-landing/app-agents-landing/div/app-helpdesk-view-ticket/div/div[2]/div/mat-card/mat-card-content/div[1]/div/mat-card/mat-card-content/div/div[1]/div/img").click()
        time.sleep(5)
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/mat-dialog-container/app-confirmation-dialog/div[3]/button[2]").click()
        logging.info("Message was deleted")
        return {
            "Test Name": "Delete Ticket",
            "Test Results": "Passed"
        }
    except Exception as e:
        logging.info("Message was not found")
        return {
            "Test Name": "Delete Ticket",
            "Test Results": "Failed"
        }