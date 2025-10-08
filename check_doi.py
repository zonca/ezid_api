import os
import requests
from dotenv import load_dotenv

def check_test_doi():
    """
    Checks the status of a test DOI using the EZID API.
    Credentials are read from EZID_USERNAME and EZID_PASSWORD environment variables.
    """
    load_dotenv() # Load environment variables from .env file

    username = os.getenv("EZID_USERNAME")
    password = os.getenv("EZID_PASSWORD")

    if not username or not password:
        print("Error: EZID_USERNAME and EZID_PASSWORD environment variables must be set.")
        return

    doi_id = "doi:10.5072/FK2/TESTDOI123"
    ezid_url = f"https://ezid.cdlib.org/id/{doi_id}"

    headers = {
        "Accept": "text/plain"
    }

    try:
        response = requests.get(
            ezid_url,
            headers=headers,
            auth=(username, password)
        )

        print(f"Request URL: {ezid_url}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text:\n{response.text}")

        response.raise_for_status()  # Raise an exception for HTTP errors
        print("DOI check successful!")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_test_doi()
