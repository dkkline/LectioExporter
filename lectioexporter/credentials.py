"""
Contains functions regarding credentials and sensitive information.
"""

from getpass import getpass
import argparse

import json

import os

from oauth2client import client, tools
from oauth2client import file as oa2c_file

from .utilities import make_dir_if_non_existant
from .config import (APPLICATION_NAME, CREDENTIALS_DIR, CLIENT_SECRET_FILE,
                     SCOPES)


def get_google_credentials():
    """
    Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    parent_parsers = [tools.argparser]
    parser = argparse.ArgumentParser(
        description=APPLICATION_NAME,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=parent_parsers)

    flags = parser.parse_args()

    make_dir_if_non_existant(CREDENTIALS_DIR)

    credential_path = os.path.join(CREDENTIALS_DIR,
                                   APPLICATION_NAME + ".json")

    store = oa2c_file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME

        credentials = tools.run_flow(flow, store, flags)

    return credentials


def get_todoist_credentials():
    """
    Gets username and password for Todoist if available,
    otherwise asks the user to input them.
    """
    make_dir_if_non_existant(CREDENTIALS_DIR)

    credentials_path = os.path.join(CREDENTIALS_DIR,
                                    "todoist.json")

    try:
        with open(credentials_path, "r") as f:
            credentials = json.load(f)

            return credentials

    except FileNotFoundError:
        user_email = input("Todoist email: ")
        user_password = getpass("Todoist password: ")

        credentials = {
            "email": user_email,
            "password": user_password
        }

        with open(credentials_path, "w") as f:
            json.dump(credentials, f)

        return credentials