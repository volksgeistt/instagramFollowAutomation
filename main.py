import time
import random
import logging
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Instagram:
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None
        self.wait = None

    def startDriver(self):
        options = uc.ChromeOptions()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = uc.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 30)

    def loginAccount(self, username, password):
        logging.info(f"Trying to login on instagram.com as : @{username}")
        self.driver.get("https://www.instagram.com/")
        time.sleep(random.uniform(4, 6))

        try:
            usernameTextArea = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            passTextArea = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            usernameTextArea.send_keys(username)
            time.sleep(random.uniform(1, 2))
            passTextArea.send_keys(password)
            time.sleep(random.uniform(1, 2))
            passTextArea.send_keys(Keys.RETURN)
            
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "svg[aria-label='Home']")))
            logging.info(f"Successfully logged in as : @{username}")
            return True
        except TimeoutException:
            logging.error(f"Login failed for username : {username}. Timed out while trying to find login elements.")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred during login as @{username}: {str(e)}")
            return False

    def openNewTabAndNavigateTo(self, url):
        logging.info(f"Opening new tab and navigating to : {url}")
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(url)
        time.sleep(random.uniform(3, 5))

    def followUserProfile(self, targetProfileUsername):
        logging.info(f"Attempting to follow user: {targetProfileUsername}")
        try:
            followButton = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Follow') or contains(@class, 'follow')]")))
            followButton.click()
            logging.info(f"Successfully clicked the follow button for {targetProfileUsername}")
            time.sleep(random.uniform(2, 4))
            return True
        except TimeoutException:
            logging.error(f"Failed to find or click the follow button for {targetProfileUsername}")
            return False
        except Exception as e:
            logging.error(f"An error occurred while trying to follow {targetProfileUsername}: {str(e)}")
            return False

    def closeScript(self):
        if self.driver:
            logging.info("Closing the followBot...")
            self.driver.quit()

def readAccounts(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def main():
    accounts = readAccounts('accounts.json')
    targetProfileUsername = "volksgeistt" # change this with the username of the account you want to follow
    followBot = Instagram(headless=False)

    for account in accounts:
        followBot.startDriver()
        username = account['username']
        password = account['password']

        try:
            if followBot.loginAccount(username, password):
                followBot.openNewTabAndNavigateTo(f"https://www.instagram.com/{targetProfileUsername}")
                if followBot.followUserProfile(targetProfileUsername):
                    logging.info(f"Successfully followed {targetProfileUsername} with account {username}")
                else:
                    logging.warning(f"Failed to follow {targetProfileUsername} with account {username}")
            else:
                logging.warning(f"Failed to log in with account {username}")
        except Exception as e:
            logging.error(f"An error occurred while processing account {username}: {str(e)}")
        finally:
            followBot.closeScript()
        time.sleep(random.uniform(3,5))

if __name__ == "__main__":
    main()
