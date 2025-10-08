import os
import requests
from dotenv import load_dotenv


def create_test_doi():
    load_dotenv()  # Load environment variables from .env file
    """
    Creates a test DOI using the EZID API.
    Credentials are read from EZID_USERNAME and EZID_PASSWORD environment variables.
    """
    username = os.getenv("EZID_USERNAME")
    password = os.getenv("EZID_PASSWORD")

    if not username or not password:
        print(
            "Error: EZID_USERNAME and EZID_PASSWORD environment variables must be set."
        )
        return

    # EZID API endpoint for creating a test DOI
    # Using a placeholder DOI for testing. In a real scenario, you'd use a shoulder.
    # For testing, EZID allows creating DOIs under 'doi:10.5072/FK2' shoulder.
    # The documentation mentions PUT to an identifier's EZID URL or POST to a shoulder.
    # Let's use PUT for a specific test DOI.
    # The documentation also mentions a test prefix 10.5072/FK2
    # Let's use a specific test DOI under this shoulder.
    doi_id = "doi:10.5072/FK2/TESTDOI123"
    ezid_url = f"https://ezid.cdlib.org/id/{doi_id}"

    # ANVL metadata for the test DOI
    # These are minimal required fields.
    metadata = {
        "datacite.creator": "Gemini CLI Agent",
        "datacite.title": "Test DOI created by Gemini CLI Agent",
        "datacite.publisher": "Google",
        "datacite.publicationyear": "2025",
        "datacite.resourcetype": "Other",
        "_profile": "datacite",
        "_target": "https://www.google.com" # A target URL is required
    }

    # Convert metadata to ANVL format
    anvl_data = ""
    for key, value in metadata.items():
        anvl_data += f"{key}: {value}\n"

    headers = {"Content-Type": "text/plain", "Accept": "text/plain"}

    try:
        response = requests.put(
            ezid_url,
            data=anvl_data.encode("utf-8"),
            headers=headers,
            auth=(username, password),
        )

        print(f"Request URL: {ezid_url}")
        print(f"Request Body:\n{anvl_data}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text:\n{response.text}")

        response.raise_for_status()  # Raise an exception for HTTP errors
        print("DOI creation successful!")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    create_test_doi()
