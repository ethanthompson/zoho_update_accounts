import json
import requests
import csv
import time

class ZohoCRMInteraction:
    def __init__(self):
        # Load client credentials from credentials.json
        with open('credentials.json') as f:
            self.credentials = json.load(f)
        self.access_token = None
        self.base_url = 'https://www.zohoapis.com/crm/v2/'
        self.client_id = self.credentials['client_id']
        self.client_secret = self.credentials['client_secret']
        self.refresh_token = self.credentials['refresh_token']

    def get_access_token(self):
        # Use refresh token to get a new access token
        token_url = 'https://accounts.zoho.com/oauth/v2/token'
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token
        }
        response = requests.post(token_url, data=data)
        response_data = response.json()
        if 'access_token' in response_data:
            self.access_token = response_data['access_token']
        else:
            raise Exception(f"Error fetching access token using refresh token: {response_data}")

    def refresh_access_token_if_needed(self):
        # Check if access token is expired or invalid and refresh it
        if not self.access_token:
            self.get_access_token()

    def update_deals_with_account(self, csv_file):
        self.refresh_access_token_if_needed()

        # Read deals.csv
        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                record_id = row.get('Record Id', '').replace('zcrm_', '')
                account_id = row.get('Account Name.id', '').replace('zcrm_', '')
                if record_id and account_id:
                    try:
                        self.update_deal_account(record_id, account_id)
                    except Exception as e:
                        print(f"Error updating deal {record_id}: {e}")
                else:
                    print(f"Missing required data for row: {row}")

    def update_deal_account(self, record_id, account_id):
        headers = {
            'Authorization': f'Zoho-oauthtoken {self.access_token}',
            'Content-Type': 'application/json'
        }
        url = f"{self.base_url}Deals/{record_id}"
        data = {
            "data": [
                {
                    "Account_Name": {
                        "id": account_id
                    }
                }
            ]
        }
        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 401:  # Unauthorized, possibly due to expired token
            print("Access token expired, refreshing...")
            self.get_access_token()
            headers['Authorization'] = f'Zoho-oauthtoken {self.access_token}'
            response = requests.put(url, headers=headers, json=data)
        if response.status_code == 200:
            print(f"Successfully updated deal {record_id} with account {account_id}")
        else:
            print(f"Failed to update deal {record_id}: {response.text}")

if __name__ == "__main__":
    crm = ZohoCRMInteraction()
    crm.update_deals_with_account('deals.csv')
