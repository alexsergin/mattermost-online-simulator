import logging
import os
import time
from random import randrange

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def set_online_status(wait_driver: WebDriverWait):
    wait_driver.until(ec.element_to_be_clickable((By.CLASS_NAME, 'status-wrapper'))).click()
    wait_driver.until(ec.element_to_be_clickable((By.ID, 'status-menu-online'))).click()


# Configure logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

options = Options()
options.headless = True

workspace_url = os.getenv('WORKSPACE_URL')
auth_login = os.getenv('AUTH_LOGIN')
auth_password = os.getenv('AUTH_PASSWORD')
end_hour = os.getenv('END_HOUR', None)
if end_hour is not None:
    end_hour = int(end_hour)
end_minutes = os.getenv('END_MINUTES', '0').split(':')

logging.info('Starting webdriver')
with webdriver.Firefox(options=options) as driver:
    wait = WebDriverWait(driver, 20)
    driver.get(workspace_url)

    # Configuring time
    if end_hour is not None:
        if len(end_minutes) > 1:
            rand_stop_minute = randrange(int(end_minutes[0]), int(end_minutes[1]))
        else:
            rand_stop_minute = int(end_minutes[0])

    # Login
    logging.info('Logging in')
    wait.until(ec.element_to_be_clickable((By.ID, 'loginId'))).send_keys(auth_login)
    wait.until(ec.element_to_be_clickable((By.ID, 'loginPassword'))).send_keys(auth_password)
    wait.until(ec.element_to_be_clickable((By.ID, 'loginButton'))).click()

    # Waiting for logged in
    while True:
        # Looking for menu
        try:
            wait.until(ec.element_to_be_clickable((By.CLASS_NAME, 'status-wrapper')))
            logging.info('Logged in')
            break
        except NoSuchElementException:
            logging.info('Awaiting for logging in')
            time.sleep(1)

    while True:
        if end_hour is not None:
            now = time.gmtime()
            if now.tm_hour >= end_hour:
                if now.tm_hour > end_hour or now.tm_min >= rand_stop_minute:
                    logging.info('It\'s time to finish work')
                    break
        set_online_status(wait)
        logging.info('Sleeping')
        time.sleep(60)

    logging.info('Shutting down')
    driver.close()
