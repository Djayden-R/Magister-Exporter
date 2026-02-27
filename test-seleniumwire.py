from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()

PASSWORD = os.getenv('PASSWORD')

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

driver.implicitly_wait(15)

# Go to the Magister Log-in page
driver.get('http://accounts.magister.net/account/login?sessionId=219ac2e652d34a8d8440c3da7b7531a8&returnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3DM6-middelharnis.magister.net%26redirect_uri%3Dhttps%253A%252F%252Fmiddelharnis.magister.net%252Foidc%252Fredirect_callback.html%26response_type%3Did_token%2520token%26scope%3Dopenid%2520profile%2520opp.read%2520opp.manage%2520attendance.overview%2520attendance.administration%2520calendar.user%2520calendar.ical.user%2520calendar.to-do.user%2520grades.read%2520grades.manage%2520oso.administration%2520registration.admin%2520lockers.administration%2520exams.administration%2520enrollment.admin%2520privacyportal.administration%26state%3D513b7b6007094502b04cb47b3c0ae736%26nonce%3Dc42a76fa80bd45f7894d4cef2a96a29a%26acr_values%3Dtenant%253Amiddelharnis.magister.net%26X-Correlation-ID%3Dmyvol7bf0y0i')

username_field = driver.find_element(By.ID, "username")

username_field.send_keys('6953')
username_field.send_keys(Keys.ENTER)

password_field = driver.find_element(By.ID, 'i0118')
password_field.send_keys(PASSWORD)
password_field.send_keys(Keys.ENTER)

submit_button = driver.find_element(By.ID, 'idSIButton9')
submit_button.click()

request = driver.wait_for_request('api/leerlingen/13807', 15)

try:
    bearer_token = request.headers['authorization']
except Exception as e:
    print(f'Error fetching token: {e}')