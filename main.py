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
import random

# Function to compare responses
def compare_responses(expected_response, actual_response):
    return expected_response.strip().lower() == actual_response.strip().lower()

# Function to store and evaluate results
def evaluate_results(results):
    overall_passed = True
    for result in results:
        question, expected, actual, passed = result
        if not passed:
            overall_passed = False
            print(f"Test Failed for Question: {question}")
            print(f"Expected Response: {expected}")
            print(f"Actual Response: {actual}")
            print("-" * 50)
    
    if overall_passed:
        print("Overall Test Result: All tests passed.")
    else:
        print("Overall Test Result: Some tests failed.")

# Function to save results to an Excel file
def save_results_to_excel(filename, results):
    df = pd.DataFrame(results, columns=["Question", "Expected Response", "Actual Response", "Test Result"])
    
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    
    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    
    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    
    # Add some cell formats.
    format_pass = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
    format_fail = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
    
    # Set the column widths.
    worksheet.set_column('A:A', 30)  # Question column
    worksheet.set_column('B:B', 40)  # Expected Response column
    worksheet.set_column('C:C', 40)  # Actual Response column
    worksheet.set_column('D:D', 15)  # Test Result column
    
    # Apply the formats to the test results.
    for row_num, result in enumerate(results, 1):
        if result[3]:  # If the test passed
            worksheet.write(row_num, 3, "Passed", format_pass)
        else:  # If the test failed
            worksheet.write(row_num, 3, "Failed", format_fail)
    
    # Close the Pandas Excel writer and output the Excel file.
    writer.close()
    print(f"Results have been saved to {filename}")

# Function to fetch the latest response
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

# Function to automate the chat testing process
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
        
        # Store the result
        results.append((question, expected_response, actual_response, passed))

        # Print the results
        print(f"Question: {question}")
        print(f"Expected Response: {expected_response}")
        print(f"Actual Response: {actual_response}")
        print(f"Test {'Passed' if passed else 'Failed'}")
        print("-" * 50)
    
    return results

# Function to automate the registration process
def automate_registration(driver, greetingmsg, name, email, phone):
    regInfo = [greetingmsg, name, email, phone]
    expectedResponses = ["Please type your name.", "Please type your email address.", "Please type your phone number.", "Your registration is successfully completed."]
    results = automate_chat_testing(driver, regInfo, expectedResponses)
    return results

def talkToAgent(driver, talkByButtonOrChat):
    talkByButtonOrChat = talkByButtonOrChat.tolower()
    questions = ["talk to an agent"]
    expected_responses = ["Please standby while I am connecting with one of our live Agent"]
    if talkByButtonOrChat == "chat":
        results = automate_registration(driver, "hi", "Mohamad", "test@example.com", "2315325412") and automate_chat_testing(driver, questions, expected_responses)
    else:
        results = automate_registration(driver, "hi", "Mohamad", "test@example.com", "2315325412d")

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

# Wait for the chat box to open for further interactions
chat_input = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Type your message...']"))
)

# Lists of questions and expected responses
questions = ["talk to an agent"]
expected_responses = ["Please standby while I am connecting with one of our live Agent"]

# Combine results
results = automate_registration(driver, "HELLO", "Mohamad", "test@example.com", "2315325412") and automate_chat_testing(driver, questions, expected_responses)

# Evaluate overall results
evaluate_results(results)

# Save results to an Excel file
currentDate = datetime.now()
formatted_date_time = currentDate.strftime("%d-%m %I.%M%p").lower()
file_name = f'chat_test_results_{formatted_date_time}.xlsx'
save_results_to_excel(file_name, results)

# Close the browser
driver.quit()
