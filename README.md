# Zoho Refresh Token Generator Script

## Overview
This script (`credentials.py`) is used to generate a refresh token for Zoho CRM using an authorization code. The refresh token can then be used by the Zoho CRM interaction script to obtain access tokens for API requests.

## Features
- Exchanges a one-time authorization code for an access token and refresh token.
- Saves the refresh token, client ID, and client secret to `credentials.json` for future use.

## Requirements
- Python 3.x
- The following Python libraries:
  - `requests` for making HTTP requests to the Zoho CRM API.

You can install the required dependencies using:
```sh
pip install requests
```

## Setup
1. **Authorization Code**: Obtain an authorization code from Zoho CRM. This can be done by setting up an app in the Zoho Developer Console and generating the code by following Zoho's OAuth flow.

2. **Client Credentials File**: Create a `self_client.json` file in the same directory as the script. This file can be generated via https://api-console.zoho.com/client/ using the self-client option. Ensure that the "Scope" for the credentials is set to "ZohoCRM.modules.ALL". The file should contain the following keys:
    ```json
    {
        "client_id": "your_client_id",
        "client_secret": "your_client_secret",
        "code": "your_authorization_code"
    }
    ```

## Running the Script
To generate the refresh token, run the script using the following command:
```sh
python credentials.py
```
This will read the `self_client.json` file, use the authorization code to obtain an access token and refresh token, and save them in a new file called `credentials.json`.

## How It Works
1. The script reads the `self_client.json` file to load the client ID, client secret, and authorization code.
2. It sends a request to Zoho's OAuth endpoint to exchange the authorization code for an access token and refresh token.
3. If successful, the refresh token is saved in `credentials.json`, along with the client ID and client secret, which are used by the main Zoho CRM script.

## Error Handling
- If the authorization code has expired or is invalid, the script will print an error message.
- Any unexpected responses from Zoho's API will also be logged to the console.

## Notes
- The authorization code provided in `self_client.json` is single-use and will expire shortly after being generated. Make sure to use it promptly.
- The `credentials.json` file should be kept secure, as it contains sensitive information necessary for accessing the Zoho CRM API.

# Zoho CRM Interaction Script

## Overview
This script is designed to update the account information of deals in Zoho CRM based on data from a CSV file. It interacts with Zoho's API to update the `Account_Name` field for each deal. The script uses credentials stored in `credentials.json` to authenticate and get an access token using a refresh token.

## Features
- Reads a CSV file (`deals.csv`) to extract deal information.
- Uses the Zoho CRM API to update the `Account_Name` field for each deal.
- Handles access token retrieval using a refresh token stored in `credentials.json`.
- Automatically refreshes the access token if it expires.

## Requirements
- Python 3.x
- The following Python libraries:
  - `requests` for making HTTP requests to the Zoho CRM API.
  - `csv` for reading the CSV file.

You can install the required dependencies using:
```sh
pip install requests
```

## Setup
1. **Credentials File**: Create a `credentials.json` file in the same directory as the script via the `credentials.py` script. The file should contain the following keys:
    ```json
    {
        "client_id": "your_client_id",
        "client_secret": "your_client_secret",
        "refresh_token": "your_refresh_token"
    }
    ```

2. **CSV File**: Prepare a `deals.csv` file in the same directory. This file should have at least the following columns:
    - `Record Id`: The unique ID of the deal (with `zcrm_` prefix).
    - `Account Name.id`: The unique ID of the account to be associated with the deal (with `zcrm_` prefix).

## Running the Script
To run the script, use the following command:
```sh
python script.py
```
Ensure that the `credentials.json` and `deals.csv` files are in the same directory as the script.

## How It Works
1. The script reads the `credentials.json` file to load the client ID, client secret, and refresh token.
2. It then obtains an access token using the refresh token.
3. The script reads the `deals.csv` file, extracting the `Record Id` and `Account Name.id` for each deal.
4. For each deal, it calls the Zoho CRM API to update the `Account_Name` field.
5. If the access token expires, it will automatically refresh the token and retry the request.

## Error Handling
- If the script cannot find the required data for a row in the CSV, it will print an error message indicating which row is missing data.
- If the access token is invalid or expired, the script will attempt to refresh it and retry the request.
- Any issues during API requests (such as network errors or permission issues) will be logged to the console.

## Notes
- Ensure that the `credentials.json` file is kept secure, as it contains sensitive information.
- The refresh token should be generated once and can be reused multiple times to obtain new access tokens.

## Troubleshooting
- **Invalid Code Error**: If you encounter an error indicating an `invalid_code`, you need to generate a new refresh token using Zoho's OAuth flow.
- **OpenSSL Warning**: If you see a warning about `urllib3` and OpenSSL, ensure your Python environment is using an up-to-date version of OpenSSL.
