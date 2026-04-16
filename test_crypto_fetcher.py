import pytest
from unittest.mock import patch, MagicMock

from crypto_fetcher import get_request_params, fetch_crypto_data

def test_get_request_params_formats_headers_correctly():
    """Tests that the URL and headers are formatted exactly as the API expects"""
    fake_key = 'test_key_123'
    
    with patch('crypto_fetcher.get_api_key', return_value=fake_key):
        url, headers = get_request_params()
        
        assert url == 'https://api.freecryptoapi.com/v1/getCryptoList'
        assert headers['Authorization'] == f'Bearer {fake_key}'
        assert headers['accept'] == '*/*'
   
        
@patch('crypto_fetcher.requests.get')
def test_fetch_crypto_data_success(mock_get):
    """Tests that a successful 200 OK response correctly returns the JSON dictionary"""
    
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {'status': 'success', 'data': ['BTC', 'ETH']}
    
    mock_get.return_value = fake_response
    
    dummy_url = 'http://fakeurl.com'
    dummy_headers = {'Authorization': "Bearer 1234"}
    
    result = fetch_crypto_data(dummy_url, dummy_headers)
    
    assert result == {'status': 'success', 'data': ['BTC', 'ETH']}
    
    mock_get.assert_called_once_with(dummy_url, headers=dummy_headers)
    
    
@patch('crypto_fetcher.requests.get')
def test_fetch_crypto_data_fail(mock_get):
    """Tests that a failed 404 NOK response returns None instead of crashing"""
    
    fake_response = MagicMock()
    fake_response.status_code = 404
    fake_response.text = 'Not Found'
    
    mock_get.return_value = fake_response
    
    dummy_url = 'http://fakeurl.com'
    dummy_headers = {}
    
    result = fetch_crypto_data(dummy_url, dummy_headers)
    
    assert result is None