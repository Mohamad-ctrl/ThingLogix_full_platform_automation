from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import pandas as pd
import logging
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import csv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to compare responses
def compare_responses(expected_response, actual_response):
    return expected_response.strip().lower() == actual_response.strip().lower()

def save_chat_results_to_excel(results, writer):
    df = pd.DataFrame(results)
    df.to_excel(writer, sheet_name='Chat Tests', index=False)

def save_agent_action_results_to_excel(results, writer):
    df = pd.DataFrame(results)
    df.to_excel(writer, sheet_name='Agent Actions', index=False)

def save_agent_messages_to_excel(results, writer):
    df = pd.DataFrame(results)
    df.to_excel(writer, sheet_name='Agent Messages', index=False)

def save_customer_details_results_to_excel(results, writer):
    df = pd.DataFrame(results)
    df.to_excel(writer, sheet_name='Customer Details Capture', index=False)

def save_post_chat_results_to_excel(results, writer):
    df = pd.DataFrame(results)
    df.to_excel(writer, sheet_name='Post Chat', index=False)

# # Function to fetch the latest response
def get_latest_response(driver):
    messages = driver.find_elements(By.CSS_SELECTOR, "#content > div[id^='message_']")
    if messages:
        # Extract the message IDs and sort them to find the latest one
        message_ids = [int(msg.get_attribute('id').split('_')[-1]) for msg in messages]
        latest_id = min(message_ids)  # Get the smallest number which represents the latest message
        latest_message = driver.find_element(By.ID, f"message_{latest_id}")
        # Check if the message is from the bot (doesn't contain the user's input class or id)
        if "UserMessage" not in latest_message.get_attribute("innerHTML"):
            return latest_message.find_element(By.CSS_SELECTOR, "span.ng-star-inserted").text
    return ""

# Functions for individual tests (simplified for illustration)
def automate_chat_testing(driver, questions, expected_responses):
    results = []  # List to store test results
    for i, question in enumerate(questions):
        chat_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Type your message...']"))
        )
        
        # Type and send each question
        chat_input.send_keys(question)
        chat_input.send_keys(Keys.RETURN)
        
        # Wait for the response to be appended to the chat
        time.sleep(10)  # Adjust the sleep time as necessary

        expected_response = expected_responses[i]
        actual_response = get_latest_response(driver)  # Call the function to get the response
        
        passed = compare_responses(expected_response, actual_response)
        
        results.append({
            "Question": question,
            "Expected Response": expected_response,
            "Actual Response": actual_response,
            "Test Result": "Passed" if passed else "Failed"
        })

    overall_result = "Pass" if all(result["Test Result"] == "Passed" for result in results) else "Fail"
    return overall_result, results

# Function to automate the registration process
def automate_registration(driver, greetingmsg, name, email, phone):
    regInfo = [greetingmsg, name, email, phone]
    expectedResponses = ["Please type your name.", "Please type your email address.", "Please type your phone number.", "Your registration is successfully completed."]
    overall_result, reg_details = automate_chat_testing(driver, regInfo, expectedResponses)
    return overall_result, reg_details

def talkToAgent(driver, talkByButtonOrChat):
    if talkByButtonOrChat == "button":
        try:
            # Wait until the chatbot container is visible and interact with it
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "chatbot-container"))
            )

            # Find the "Talk To Agent" button by its text
            talk_to_agent_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//button[contains(., 'Talk To Agent')]"))
            )
            
            # Click the "Talk To Agent" button
            talk_to_agent_button.click()
            
            # Wait for the response after clicking the button
            time.sleep(10)
            latest_response = get_latest_response(driver)
            logging.info(f"Latest response: {latest_response}")
            
            # Expected response after clicking the button
            expected_response = "Please standby while I am connecting with one of our live Agent"
            if compare_responses(expected_response, latest_response):
                result = "Pass"
            else:
                result = "Fail"
            agent_details = {"Test name": "talk to agent", "Action": talkByButtonOrChat, "Test Result": result}
            return result, agent_details
        
        except Exception as e:
            logging.error(f"Error occurred while trying to click the 'Talk To Agent' button: {e}")
            return "Fail", {
                "Action": "Talk to Agent Button",
                "Expected Response": expected_response,
                "Actual Response": str(e),
                "Passed": False
            }

def loginAsAgent(driver, uatEmail, uatPassword, awsUsername, awsPassword, awsURL):
    try:
        # Store the current window handle
        initial_window = driver.current_window_handle
        logging.info(f"Initial window handle: {initial_window}")

        # Open a new tab and navigate to the login page
        driver.execute_script("window.open('https://uat.thinglogixce.app');")
        logging.info("Opened a new tab with the login page")

        # Switch to the new tab (uat.thinglogixce.app)
        driver.switch_to.window(driver.window_handles[1])

        # Wait for the first login form to load and input credentials
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        driver.find_element(By.ID, "username").send_keys(uatEmail)
        driver.find_element(By.ID, "password").send_keys(uatPassword)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        logging.info("Entered first set of credentials and clicked submit")

        time.sleep(25)

        # Open another new tab
        driver.execute_script("window.open('');")
        logging.info("Opened another new tab")

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[2])

        # Navigate to the specified URL in the new tab
        driver.get(awsURL)
        
        # Wait for the login form to appear and input credentials
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "wdc_username"))
        )
        driver.find_element(By.ID, "wdc_username").send_keys(awsUsername)
        driver.find_element(By.ID, "wdc_password").send_keys(awsPassword)
        driver.find_element(By.ID, "wdc_login_button").click()
        logging.info("Entered credentials and clicked login in the new tab")
        time.sleep(10)

        # Switch back to the uat.thinglogixce.app tab
        driver.switch_to.window(driver.window_handles[1])
        logging.info("Switched back to the uat.thinglogixce.app tab")

        # Refresh the uat.thinglogixce.app tab
        driver.refresh()
        logging.info("Page refreshed")
        time.sleep(5)

        # Close the second tab (thinglogixce-new)
        driver.switch_to.window(driver.window_handles[2])
        driver.close()
        logging.info("Closed the second tab")

        # Switch back to the uat.thinglogixce.app tab to continue further actions if any
        driver.switch_to.window(driver.window_handles[1])
        return "Pass"
    except Exception as e:
        logging.error(f"Error during loginAsAgent: {e}", exc_info=True)
        driver.save_screenshot("login_as_agent_error.png")
        logging.info("Screenshot captured: login_as_agent_error.png")
        return "Fail"
    finally:
        # Switch back to the initial window
        driver.switch_to.window(initial_window)
        logging.info("Switched back to the initial window")

# Define the function to wait for and click the "accept call" button
def wait_and_click_accept(driver, timeout=30):
    try:
        accept_button = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.ID, 'agent-incoming-call-accept'))
        )
        accept_button.click()
        logging.info("Accepted the call.")
        return "Pass", {"Action": "Accept Call", "Passed": True}
    except Exception as e:
        logging.info(f"Error while accepting call: {e}")
        return "Fail", {"Action": "Accept Call", "Passed": False, "Error": str(e)}

# Define the function to wait for and click the "reject call" button
def wait_and_click_reject(driver, timeout=30):
    try:
        reject_button = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.ID, 'agent-incoming-call-reject'))
        )
        reject_button.click()
        logging.info("Rejected the call.")
        return "Pass", {"Action": "Reject Call", "Passed": True}
    except Exception as e:
        logging.info(f"Error while rejecting call: {e}")
        return "Fail", {"Action": "Reject Call", "Passed": False, "Error": str(e)}

def acceptOrReject(driver, action):
    results = []
    if action == "accept":
        result, details = wait_and_click_accept(driver)
        results.append(details)
    elif action == "reject":
        result, details = wait_and_click_reject(driver)
        results.append(details)
    elif action == "both":
        reject_result, reject_details = wait_and_click_reject(driver)
        results.append(reject_details)
        time.sleep(10)
        accept_result, accept_details = wait_and_click_accept(driver)
        results.append(accept_details)
    action_details = {"Test name": "accept or reject", "Action": action, "Test Result": result}
    return result, action_details

# Function to send messages as an agent and verify responses
def send_message_as_agent(driver, messages):
    results = []  # List to store test results
    for message in messages:
        driver.switch_to.window(driver.window_handles[1])
        # Send message as an agent
        chat_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea#agent-chat-details-type-area"))
        )
        chat_input.send_keys(message)
        send_button = driver.find_element(By.CSS_SELECTOR, "button#agent-chat-details-send-message")
        send_button.click()
        
        # Wait for the message to be sent
        time.sleep(5)  # Adjust as necessary
        
        # Verify the received message
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(5)
        received_message = get_latest_response(driver)
        message_details = [{"Test name": "send message as agent", "Message": msg, "Latest User Message": "Latest User Message", "Test Result": "Passed"} for msg in messages]
        message_result = compare_responses(message, received_message)
        return message_result, message_details

def send_attachment_as_agent(driver, file_path):
    try:
        # Ensure the file exists
        if not os.path.isfile(file_path):
            logging.error(f"File not found: {file_path}")
            return "Fail", {"Action": "Send Attachment", "Passed": False, "Error": "File not found"}
        
        # Locate the file input element
        file_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'conversationAttachments'))
        )
        
        # Send the file path to the input element
        file_input.send_keys(file_path)
        logging.info(f"File path sent to input: {file_path}")

        # Optionally, trigger the send action if needed
        send_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, 'agent-chat-details-send-message'))
        )
        send_button.click()
        logging.info("Send button clicked")
        
        # Add any necessary wait or verification steps here
        time.sleep(5)  # Adjust sleep time as necessary for the file upload to complete
        
        # Retrieve and log the latest response
        latest_response = get_latest_response(driver)
        attachment_result = "Passed"
        attachment_details = {"Test name": "send attachment as agent", "Message": "Image", "Latest User Message": "Image", "Test Result": attachment_result}
        return attachment_result, attachment_details
    
    except Exception as e:
        logging.error(f"Error while sending attachment: {e}", exc_info=True)
        return "Fail", {
            "Action": "Send Attachment",
            "Passed": False,
            "Error": str(e)
        }
    
def fill_description_and_post(driver, description):
    try:
        comment_textarea = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[formcontrolname='comment']"))
        )
        
        # Fill out the description
        comment_textarea.send_keys(description)
        logging.info(f"Description filled: {description}")

        # Wait for the "Post" button to be enabled
        post_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tl-ce-submit[type='submit']"))
        )
        
        # Click the "Post" button
        post_button.click()
        logging.info("Post button clicked")

        # Add any necessary wait or verification steps here
        WebDriverWait(driver, 30).until(
            EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "textarea[formcontrolname='comment']"), "")
        )
        logging.info("Comment posted successfully")
        description_result = "Passed"
        description_details = {"Test name": "fill description and post", "Test Result": description_result}
        return description_result, description_details
    
    except Exception as e:
        logging.error(f"Error while posting description: {e}", exc_info=True)
        return "Fail", {
            "Action": "Post Description",
            "Description": description,
            "Passed": False,
            "Error": str(e)
        }
    
def capture_and_compare_customer_details(driver):
    try:
        # Capture customer details before accepting the call
        customerDetailsBefore = capture_pre_accept_details(driver)
        logging.info(f"Customer details before accepting the call: {customerDetailsBefore}")

        time.sleep(5)

        # Wait for and click the "accept call" button
        wait_and_click_accept(driver)

        time.sleep(10)
        # Capture customer details after accepting the call
        customerDetailsAfter = capture_post_accept_details(driver)
        logging.info(f"Customer details after accepting the call: {customerDetailsAfter}")

        # Compare the customer details
        # details_match = customerDetailsBefore == customerDetailsAfter
        if customerDetailsAfter == customerDetailsBefore:
            details_match = "Pass"
        else:
            details_match = "Fail"
        result = "Pass" if details_match else "Fail"
        
        return result, {
            "Action": "Capture and Compare Customer Details",
            "Customer Details Before": customerDetailsBefore,
            "Customer Details After": customerDetailsAfter,
            "Passed": details_match
        }

    except Exception as e:
        logging.error(f"Error in capturing and comparing customer details: {e}", exc_info=True)
        return "Fail", {
            "Action": "Capture and Compare Customer Details",
            "Error": str(e),
            "Passed": False
        }
    
def capture_pre_accept_details(driver):
    try:
        # Wait until the elements are visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div/mat-dialog-container/app-contact-incoming/mat-dialog-content/div/p[3]")))
        
        # Capture pre-accept details using XPath
        name = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/mat-dialog-container/app-contact-incoming/mat-dialog-content/div/p[3]").text.strip()
        phone_number = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/mat-dialog-container/app-contact-incoming/mat-dialog-content/div/p[5]").text.strip()
        website = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/mat-dialog-container/app-contact-incoming/mat-dialog-content/div/p[6]").text.strip()
        
        return {
            "name": name,
            "phone_number": phone_number,
            "website": website
        }
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error in capturing pre-accept details: {str(e)}")
        return None


def capture_post_accept_details(driver):
    try:
        name = driver.find_element(By.CSS_SELECTOR, "p.tl-ce-card-title.tl-ce-colored.text-center").text.strip()
        website = driver.find_elements(By.CSS_SELECTOR, "p.tl-ce-card-subtitle.text-center")[0].text.strip()
        phone_number = driver.find_elements(By.CSS_SELECTOR, "p.tl-ce-card-subtitle.text-center")[1].text.strip()
        logging.info(f"name: {name}\nphone: {phone_number}\nwebsite: {website}")

        return {
        "name": name,
        "phone_number": phone_number,
        "website": website
    }
    except Exception as e:
        logging.error(f"Error in capturing post-accept details: {e}", exc_info=True)
        return {}
    
def end_agent_chat(driver):
    driver.switch_to.window(driver.window_handles[1])
    close_button = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-agent-chat-history-tabs/span/span/mat-tab-group/mat-tab-header/div[2]/div/div/div/div/button")
    close_button.click()
    time.sleep(5)
    return "Pass"
    
def change_customer_feedback(driver):
    feedback_options = {
        "Positive": "//*[@id='mat-tab-content-1-0']/div/app-agent-chat-history/div/div/div/div[2]/app-customer-details-card/div/form/div[3]/div[1]/div/select/option[1]",
        "Neutral": "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-agent-chat-history-tabs/span/span/mat-tab-group/div/mat-tab-body/div/app-agent-chat-history/div/div/div/div[2]/app-customer-details-card/div/form/div[3]/div[1]/div/select/option[2]",
        "Negative": "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-agent-chat-history-tabs/span/span/mat-tab-group/div/mat-tab-body/div/app-agent-chat-history/div/div/div/div[2]/app-customer-details-card/div/form/div[3]/div[1]/div/select/option[3]"
    }

    results = []

    for feedback_label, feedback_xpath in feedback_options.items():
        try:
            # Click on the edit button
            edit_button = driver.find_element(By.XPATH, "//*[@id='mat-tab-content-1-0']/div/app-agent-chat-history/div/div/div/div[2]/app-customer-details-card/div/form/div[3]/div[3]/button")
            edit_button.click()

            # Select the feedback option
            feedback_select = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-agent-chat-history-tabs/span/span/mat-tab-group/div/mat-tab-body/div/app-agent-chat-history/div/div/div/div[2]/app-customer-details-card/div/form/div[3]/div[1]/div/select")
            feedback_select.click()

            feedback_option = driver.find_element(By.XPATH, feedback_xpath)
            feedback_option.click()

            # Click on the save button
            save_button = driver.find_element(By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-agent-chat-history-tabs/span/span/mat-tab-group/div/mat-tab-body/div/app-agent-chat-history/div/div/div/div[2]/app-customer-details-card/div/form/div[3]/div[3]/button[1]")
            save_button.click()

            # Validate that the feedback has been changed
            current_feedback = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-agent-chat-history-tabs/span/span/mat-tab-group/div/mat-tab-body/div/app-agent-chat-history/div/div/div/div[2]/app-customer-details-card/div/form/div[3]/div[1]/div/span[2]"))
            ).text.strip()

            if current_feedback == feedback_label:
                results.append({
                    "Feedback Label": feedback_label,
                    "Action": "Change Customer Feedback",
                    "Message": "Feedback successfully changed",
                    "Passed": True
                })
            else:
                results.append({
                    "Feedback Label": feedback_label,
                    "Action": "Change Customer Feedback",
                    "Message": "Feedback change validation failed",
                    "Passed": False
                })

        except Exception as e:
            results.append({
                "Feedback Label": feedback_label,
                "Action": "Change Customer Feedback",
                "Message": f"Error in changing feedback: {str(e)}",
                "Passed": False
            })

    feedback_details = [{"Test name": "change customer feedback", "Test Result": "Passed"}]
    return results, feedback_details

def get_latest_agent_response():
    try:
        # Wait for the messages container to be present
        messages_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="msg-container"]'))
        )
        
        # Find all agent messages
        agent_messages = messages_container.find_elements(By.XPATH, './/div[contains(@class, "tl-ce-agent-message")]')
        
        if not agent_messages:
            print("No agent messages found.")
            return None
        
        # Get the last agent message
        latest_message = agent_messages[-1]
        
        # Extract the text from the message
        message_text = latest_message.find_element(By.XPATH, './/div[contains(@class, "tl-ce-chat-message-text")]').text
        
        return message_text
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def send_predefined_message(driver, predefined_message_xpath):
    try:
        # Click on the Predefined Image Button
        predefined_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="agent-chat-details-canned-messages"]'))
        )
        predefined_button.click()
        logging.info("Clicked on the Predefined Image Button.")

        # Change language to English (default language)
        language_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-sidenav/mat-drawer-container/mat-drawer-content/app-agent-chat-history-tabs/span/span/mat-tab-group/div/mat-tab-body/div/app-agent-chat-history/div/div/div/div[1]/div/div[5]/app-predefined-messages-list/div/div[1]/mat-form-field'))
        )
        language_button.click()
        logging.info("Opened the language selection list.")

        # Choose English from the dropdown list (assuming English is already selected by default)
        # If not selected by default, additional steps to choose English should be added here.

        # Pick the predefined text to send
        predefined_message = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, predefined_message_xpath))
        )
        predefined_message.click()
        logging.info("Selected the predefined message.")

        # Press Enter to send the message
        action = webdriver.ActionChains(driver)
        action.send_keys(Keys.RETURN).perform()
        logging.info("Sent the predefined message.")

    except Exception as e:
        logging.error(f"Error during send_predefined_message: {e}", exc_info=True)
        driver.save_screenshot("send_predefined_message_error.png")
        logging.info("Screenshot captured: send_predefined_message_error.png")

# Main function to run the live chat tests
def live_chat(driver, Regname, RegEmai, RegPhone, uatUserName, uatPassWord, awsUserName, awsPassWord, awsURL, file_path, description):
    chat_results = []
    agent_action_results = []
    agent_message_results = []
    customer_details_results = []
    post_chat_results = []

    # agent uat tab[1]
    loginAsAgent(driver, uatUserName, uatPassWord, awsUserName, awsPassWord, awsURL)
    # Switching back to the chat tab[0]
    driver.switch_to.window(driver.window_handles[0])

    logging.info("Registering...")
    reg_result, reg_details = automate_registration(driver, "hi", Regname, RegEmai, RegPhone)
    chat_results.extend(reg_details)

    time.sleep(5)

    logging.info("Testing the talk to agent button")
    agent_result, agent_details = talkToAgent(driver, "button")
    agent_action_results.append(agent_details)

    # Switching to the agent uat site
    driver.switch_to.window(driver.window_handles[1])

    logging.info("Testing rejecting call")
    action_result, action_details = acceptOrReject(driver, "reject")
    agent_action_results.append(action_details)

    time.sleep(10)

    logging.info("Capturing caller information and testing accepting the call")
    capture_result, capture_details = capture_and_compare_customer_details(driver)
    customer_details_results.append(capture_details)

    time.sleep(5)

    logging.info("Testing sending a message as an agent")
    messages = ["Hi there!", "How can I assist you today?", "Let me know if you have any questions."]
    message_result, message_details = send_message_as_agent(driver, messages)
    agent_message_results.extend(message_details)

    driver.switch_to.window(driver.window_handles[1])

    logging.info("Testing sending attachment as an agent")
    attachment_result, attachment_details = send_attachment_as_agent(driver, file_path)
    agent_message_results.append(attachment_details)

    time.sleep(5)

    logging.info("Testing changing customer's feedback")
    feedback_result, feedback_details = change_customer_feedback(driver)
    post_chat_results.extend(feedback_details)

    time.sleep(5)

    logging.info("Testing posting description")
    description_result, description_details = fill_description_and_post(driver, description)
    post_chat_results.append(description_details)

    time.sleep(5)

    end_agent_chat(driver)
    post_chat_results.append({"Test name": "end chat", "Test Result": "Passed"})

    # Save results to an Excel file
    result_file = r'C:\Users\Mohamad\Desktop\live_chat_test_results.xlsx'
    with pd.ExcelWriter(result_file, mode='w', engine='openpyxl') as writer:
        save_chat_results_to_excel(chat_results, writer)
        save_agent_action_results_to_excel(agent_action_results, writer)
        save_agent_messages_to_excel(agent_message_results, writer)
        save_customer_details_results_to_excel(customer_details_results, writer)
        save_post_chat_results_to_excel(post_chat_results, writer)

    overall_result = "Pass" if all(detail.get("Test Result", "Failed") == "Passed" for detail in chat_results) else "Fail"
    return overall_result, result_file

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

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

file_path = "C:\\Users\\Mohamad\\Desktop\\login_as_agent_error.png"
awsLink = "https://thinglogixce-new.awsapps.com/auth/?client_id=e5d4030c01266747&redirect_uri=https%3A%2F%2Fthinglogixce-new.my.connect.aws%2Fauth%2Fcode%3Fdestination%3D%252Fccp-v2%252F&state=wMjrRvhUw2n3lAZL0s_Vjl14SyAZuCYdsWyRoV-nKLwTm61MLbfV4bZ67RtZ6A5ZDjWAS3jQy5bA_G1R_WMvnA"

# driver, url, greetingmsg, name, email, phone, talkByButtonOrChat, action, messages, file_path, description
overall_result, result_file = live_chat(driver, "Mohamad", "test@example.com", "02341823945", "rida@thinglogix.com", "123", "test-uat", "Test@123", awsLink, file_path, "Test Description")
# save_results(results)
print(f"Overall Result: {overall_result}")
print(f"Test results saved to: {result_file}")
driver.quit()
