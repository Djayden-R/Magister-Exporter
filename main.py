import json
import logging
from fetch_magister import fetch_magister_calendar, fetch_magister_token
from pathlib import Path

PROGRAM_PATH = Path("/usr/src/app")
OPTIONS_FILE_PATH = "/data/options.json"

def get_credentials():
    with open(OPTIONS_FILE_PATH, 'r') as f:
        options = json.load(f)

    # Load dictionary with credentials
    # Expected format: [{'username': username, 'password': password}, ...]
    credentials_list: list[dict] = options['credentials']

    return credentials_list

def get_tokens():
    token_path = PROGRAM_PATH / "tokens.json"

    if token_path.exists():
        with open(token_path, 'r') as f:
            pass
    else:
        open(token_path, 'x') # Create tokens file


def main():
    credentials_list = get_credentials()

    for credenials in credentials_list:
        username = credenials.get('username', None)
        password = credenials.get('password', None)

        if not(username and password):
            logging.error(f"Invalid credentials found (username={username}, password={password})")
            continue





    if credentials_list:
        pass
    else:
        logging.warning("Credentials not defined, exiting program...")