import requests

def fetch_digilocker_docs(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(
        "https://api.digitallocker.gov.in/public/oauth2/1/user",
        headers=headers
    )
    return response.json()