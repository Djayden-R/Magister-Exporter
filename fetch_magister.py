import requests
import json
from datetime import datetime, timedelta
from seleniumwire import webdriver  # Import from seleniumwire
from seleniumwire.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import logging

def fetch_magister_token(username, password, headless = True):
    if headless:
        # Make browser headless
        options = ChromeOptions()
        options.add_argument("--headless=new")

        # Create a new instance of the Chrome driver with headless options
        driver = webdriver.Chrome(options=options)
    else:

        driver = webdriver.Chrome()

    # Make browser wait a maximum of 15 seconds when searching for elements
    driver.implicitly_wait(15)

    # Go to the Magister Log-in page
    logging.debug("Going to Magister")
    driver.get('http://accounts.magister.net/account/login?sessionId=219ac2e652d34a8d8440c3da7b7531a8&returnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3DM6-middelharnis.magister.net%26redirect_uri%3Dhttps%253A%252F%252Fmiddelharnis.magister.net%252Foidc%252Fredirect_callback.html%26response_type%3Did_token%2520token%26scope%3Dopenid%2520profile%2520opp.read%2520opp.manage%2520attendance.overview%2520attendance.administration%2520calendar.user%2520calendar.ical.user%2520calendar.to-do.user%2520grades.read%2520grades.manage%2520oso.administration%2520registration.admin%2520lockers.administration%2520exams.administration%2520enrollment.admin%2520privacyportal.administration%26state%3D513b7b6007094502b04cb47b3c0ae736%26nonce%3Dc42a76fa80bd45f7894d4cef2a96a29a%26acr_values%3Dtenant%253Amiddelharnis.magister.net%26X-Correlation-ID%3Dmyvol7bf0y0i')

    logging.debug("Entering name")
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(username)
    username_field.send_keys(Keys.ENTER)

    logging.debug("Entering password")
    password_field = driver.find_element(By.ID, 'i0118')
    password_field.send_keys(password)
    password_field.send_keys(Keys.ENTER)

    logging.debug("Pressing button")
    submit_button = driver.find_element(By.ID, 'idSIButton9')
    submit_button.click()

    request = driver.wait_for_request('api/leerlingen/', 15)
    bearer_token = request.headers['authorization']
    logging.debug(f"Got bearer token{bearer_token[:20]}...")

    user_id = request.url.split('api/leerlingen/')[1]
    if "/" in user_id:
        user_id = user_id.split("/")[0]
    
    return user_id,  bearer_token

def fetch_magister_calendar(user_id, bearer_token, days_to_fetch):
    headers = {
        "Authorization": bearer_token,
        "content-type": "application/json"
    }

    current_date = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=days_to_fetch)).strftime("%Y-%m-%d")

    url = f"https://middelharnis.magister.net/api/personen/{user_id}/afspraken?status=1&tot={end_date}&van={current_date}"

    r = requests.get(url, headers=headers)

    if r.ok:
        calendar = json.loads(r.text)
        return calendar
    else:
        return None