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
