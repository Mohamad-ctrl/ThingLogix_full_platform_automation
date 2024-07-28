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


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')# Function to compare responses

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

def save_report_results(results, writer):
    df = pd.DataFrame(results)
    df.to_excel(writer, sheet_name='Report Results', index=False)

def save_canned_megs_results(results, writer):
    df = pd.DataFrame(results)
    df.to_excel(writer, sheet_name='Canned Messages Results', index=False)

def save_help_desk_tests_results(results, writer):
    df = pd.DataFrame(results)
    df.to_excel(writer, sheet_name='Helpdesk Results', index=False)

# Main function to run the live chat tests
def live_chat(driver, Regname, RegEmai, RegPhone, uatUserName, uatPassWord, awsUserName, awsPassWord, awsURL, file_path, description):
    chat_results = []
    agent_action_results = []
    agent_message_results = []
    customer_details_results = []
    post_chat_results = []

    # agent uat tab[1]
    auth.loginAsAgent(driver, uatUserName, uatPassWord, awsUserName, awsPassWord, awsURL)
    # Switching back to the chat tab[1]]
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(10)
    utils.set_agent_as_avalible(driver)
    time.sleep(5)
    # Switching back to the chat tab[0]
    driver.switch_to.window(driver.window_handles[0])

    logging.info("Registering...")
    reg_result, reg_details = utils.automate_registration(driver, "hi", Regname, RegEmai, RegPhone)
    chat_results.extend(reg_details)

    time.sleep(5)

    logging.info("Testing the talk to agent button")
    agent_result, agent_details = utils.talkToAgent(driver, "button")
    agent_action_results.append(agent_details)

    # Switching to the agent uat site
    driver.switch_to.window(driver.window_handles[1])

    logging.info("Testing rejecting call")
    action_result, action_details = utils.acceptOrReject(driver, "reject")
    agent_action_results.append(action_details)

    time.sleep(10)

    logging.info("Capturing caller information and testing accepting the call")
    capture_result, capture_details = utils.capture_and_compare_customer_details(driver)
    customer_details_results.append(capture_details)

    time.sleep(5)

    logging.info("Testing sending a message as an agent")
    messages = ["Hi there!", "How can I assist you today?", "Let me know if you have any questions."]
    message_result, message_details = utils.send_message_as_agent(driver, messages)
    agent_message_results.extend(message_details)

    driver.switch_to.window(driver.window_handles[1])

    # time.sleep(5)
    # logging.info("Testing the predefined messages")
    # send_predefined_message_result, send_predefined_message_details = send_predefined_message(driver)
    # agent_message_results.append(send_predefined_message_details)

    logging.info("Testing sending attachment as an agent")
    time.sleep(5)
    attachment_result, attachment_details = utils.send_attachment_as_agent(driver, file_path)
    agent_message_results.append(attachment_details)

    time.sleep(5)

    logging.info("Testing changing customer's feedback")
    feedback_result, feedback_details = utils.change_customer_feedback(driver)
    post_chat_results.extend(feedback_details)

    time.sleep(5)

    logging.info("Testing posting description")
    description_result, description_details = utils.fill_description_and_post(driver, description)
    post_chat_results.append(description_details)

    time.sleep(5)

    utils.end_agent_chat(driver)
    driver.switch_to.window(driver.window_handles[0])
    if utils.get_latest_response(driver) == "Agent left the chat.":
        post_chat_results.append({"Test name": "end chat", "Test Result": "Passed"})
    else:
        post_chat_results.append({"Test name": "end chat", "Test Result": "Failed"})

    # Save results to an Excel file
    # Generate the current date and time
    currentDate = datetime.now()

    # Format the date and time
    formatted_date_time = currentDate.strftime("%d-%m_%I.%M%p").lower()

    # Create the file name
    file_name = f'chat_test_results_{formatted_date_time}.xlsx'

    # Get the directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the full file path
    result_file = os.path.join(script_directory, file_name)

    with pd.ExcelWriter(result_file, mode='w', engine='openpyxl') as writer:
        save_chat_results_to_excel(chat_results, writer)
        save_agent_action_results_to_excel(agent_action_results, writer)
        save_agent_messages_to_excel(agent_message_results, writer)
        save_customer_details_results_to_excel(customer_details_results, writer)
        save_post_chat_results_to_excel(post_chat_results, writer)

    overall_result = "Pass" if all(detail.get("Test Result", "Passed") == "Passed" for detail in chat_results) else "Fail"
    return overall_result, result_file

def reports_tests(driver, uatAgentEmail, uatAgentPassword, awsUsername, awsPassword, awsLink, adminEmail, adminPassword, firstRate, secondRate, thirdRate):
    results = []
    
    # auth.loginAsAgent(driver, uatAgentEmail, uatAgentPassword, awsUsername, awsPassword, awsLink)
    # time.sleep(15)
    # driver.switch_to.window(driver.window_handles[1])
    # utils.set_agent_as_avalible(driver)
    # time.sleep(10)
    # driver.switch_to.window(driver.window_handles[0])
    
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

# Initialize WebDriver
service = Service('C:/Users/Mohammad/.wdm/drivers/chromedriver/win64/127.0.6533.72/chromedriver.exe')
driver = webdriver.Chrome(service=service)

# The website URL
chat_url = "https://dqt6e7ekz6j0s.cloudfront.net/"

# Open the website
driver.get(chat_url)

driver.maximize_window() 

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
# overall_result, result_file = live_chat(driver, "Mohamad", "test@example.com", "02341823945", "rida@thinglogix.com", "123", "test-uat", "Test@123", awsLink, file_path, "Test Description")
# print(f"Overall Result: {overall_result}")
# print(f"Test results saved to: {result_file}")


# Reports tests
# result_file = reports_tests(driver, "rida@thinglogix.com", "123", "test-uat", "Test@123", awsLink, "maria+uat@thinglogix.com", "MZ@12345", "3", "5", "3")
# print(f"Test results saved to: {result_file}")

# Canned messages tests
# replyT = "Test Reply"
# caseNameT = "Test Case Name"
# newReplyT = "New test reply"
# newCaseNameT = "New case name"
# result_file = cannedMessages(driver, caseNameT, replyT, newReplyT, newCaseNameT, "maria+uat@thinglogix.com", "MZ@12345")
# print(f"Test results saved to: {result_file}")

# Helpdesk Tests
# result_file = helpDiskTests(driver)
# print(f"Test results saved to: {result_file}")

engagement.run_channels_tests(driver)

    
time.sleep(3000)
driver.quit()
