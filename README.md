# EZID DOI Management

This project provides Python scripts to interact with the EZID API for creating and checking Digital Object Identifiers (DOIs).

## Setup

### 1. Clone the Repository (if not already done)

```bash
git clone <repository_url>
cd ezid_api
```

### 2. Configure Credentials

Create a `.env` file in the root of the project to store your EZID username and password. Replace the placeholder values with your actual credentials.

```dotenv
EZID_USERNAME="your_ezid_username"
EZID_PASSWORD="your_ezid_password"
```

**Note**: The `.env` file is ignored by Git to prevent sensitive information from being committed to version control.

### 3. Install Dependencies

It is recommended to use `uv` for managing your Python virtual environment and dependencies.

```bash
# Create a virtual environment
uv venv

# Install required Python packages
uv pip install -r requirements.txt
```

## Usage

### 1. Create a Test DOI

The `create_doi.py` script will create a test DOI using the EZID API. It reads your credentials from the `.env` file.

```bash
uv run python create_doi.py
```

Upon successful creation, you will see a `201 Created` response and the DOI identifier.

### 2. Check the Status of a Test DOI

The `check_doi.py` script allows you to retrieve the metadata for a specific test DOI from the EZID API.

```bash
uv run python check_doi.py
```

This will output the metadata associated with the DOI, confirming its existence and details.

## Verifying in a Web Browser

You can verify the DOI's creation and its associated information directly in a web browser:

### 1. View DOI Metadata on EZID

To see the raw metadata that EZID stores for your DOI, navigate to the following URL in your browser:

`https://ezid.cdlib.org/id/doi:10.5072/FK2/TESTDOI123`

### 2. Resolve the DOI

The DOI itself can be resolved through a standard DOI resolver. Since the `_target` URL for the created DOI is set to `https://www.google.com`, entering the following into your browser will redirect you to Google:

`https://doi.org/10.5072/FK2/TESTDOI123`
