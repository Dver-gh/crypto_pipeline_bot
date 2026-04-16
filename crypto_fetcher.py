import os
from dotenv import load_dotenv
from datetime import datetime
import json
import requests

def get_api_key() -> str:
    """Gets an api key from .env file

    Returns:
        str: Api key
    """
    load_dotenv()
    return os.getenv("CRYPTO_API_KEY")
    
    
def get_request_params() -> tuple[str, dict]:
    """Makes a request for data currency from api
    
    Returns:
        str: url address for request
        str: headers for request
    """
    
    url = "https://api.freecryptoapi.com/v1/getCryptoList"
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_api_key()}'
    }
    return url, headers
    
    
def fetch_crypto_data(url: str, headers: dict) -> dict | None:
    """Makes the API request and returns the JSON data if successful

    Args:
        url (str): url address for request
        headers (dict): headers for request

    Returns:
        dict | None: whole JSON data from request or None if failed
    """
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print(f'Fetch successful!')
            return response.json()
        else:
            print(f'Fetch unsuccessful, status code: {response.status_code}')
            print(response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f'Exception occured during request: {e}')
        return None


def save_data_to_json(data: dict, folder_path: str = './fetched_data') -> None:
    """Saves a dictionary to a JSON file with today's date

    Args:
        data (dict): JSON data to be saved
        folder_path (str, optional): Path to the location where file should be stored. Defaults to './fetched_data'.
    """
    
    filename = f'data_{datetime.now().date()}.json'
    filepath = os.path.join(folder_path, filename)
    
    os.makedirs('./fetched_data', exist_ok=True)
    
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        print(f'Data saved successfully to {filepath}')
    except Exception as e:
        print(f'Exception occured while saving the data to file: {e}')
  
    
def main():
    """Orchestrator function"""
    url, header = get_request_params()
    
    crypto_data = fetch_crypto_data(url, header)
    
    if crypto_data is not None:
        save_data_to_json(crypto_data)
    else:
        print('Fetch failure happened, aborting save process')


if __name__ == "__main__":
    main()