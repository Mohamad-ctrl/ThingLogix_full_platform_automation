from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
import utils

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def loginAsAdmin(driver, uatEmail, uatPassword):
    try:
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
        return "Pass"
    except Exception as e:
        logging.error(f"Error during loginAsAdmin: {e}", exc_info=True)
        driver.save_screenshot("login_as_admin_error.png")
        logging.info("Screenshot captured: login_as_admin_error.png")
        return "Fail"
    
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

        time.sleep(35)

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
        time.sleep(20)

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

