import json
import requests

class ZohoRefreshTokenGenerator:
    def __init__(self):
        # Load client credentials from self_client.json
        with open('self_client.json') as f:
            self.credentials = json.load(f)
        self.client_id = self.credentials['client_id']
        self.client_secret = self.credentials['client_secret']
        self.grant_code = self.credentials['code']
        self.redirect_uri = 'https://www.yourredirecturi.com'

    def generate_refresh_token(self):
        # Exchange grant code for access token and refresh token
        token_url = 'https://accounts.zoho.com/oauth/v2/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': self.grant_code,
            'redirect_uri': self.redirect_uri
        }
        response = requests.post(token_url, data=data)
        response_data = response.json()

        if 'refresh_token' in response_data:
            refresh_token = response_data['refresh_token']
            # Save the refresh token and other necessary credentials in credentials.json
            credentials = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'refresh_token': refresh_token
            }
            with open('credentials.json', 'w') as f:
                json.dump(credentials, f)
            print("Refresh token and credentials saved successfully in credentials.json.")
        elif 'error' in response_data:
            print(f"Error fetching refresh token: {response_data['error']}, {response_data.get('error_description', 'No description available')}")
        else:
            raise Exception(f"Unexpected response: {response_data}")

if __name__ == "__main__":
    generator = ZohoRefreshTokenGenerator()
    generator.generate_refresh_token()
