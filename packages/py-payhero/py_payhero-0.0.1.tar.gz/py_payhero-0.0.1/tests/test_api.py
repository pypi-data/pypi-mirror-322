import pytest
from unittest.mock import patch
from PayHero.main import API  # Adjust the import based on your package structure
from dotenv import load_dotenv
from os import environ
load_dotenv() 


@pytest.fixture
def api_instance():
    """Fixture to create an API instance for testing."""
    api_username = environ.get('TESTS_USERNAME')
    api_password = environ.get('TESTS_PASSWORD')
    return API(api_username, api_password)

def test_get_service_balance(api_instance, mocker):
    """Test the get_service_balance method."""
    mock_response = {
        "balance": 100.0
    }
    mocker.patch('requests.get', return_value=mocker.Mock(status_code=200, json=lambda: mock_response))

    response = api_instance.get_service_balance()
    assert response == mock_response

def test_get_payment_balance(api_instance, mocker):
    """Test the get_payment_balance method."""
    mock_response = {
        "balance": 50.0
    }
    mocker.patch('requests.get', return_value=mocker.Mock(status_code=200, json=lambda: mock_response))

    response = api_instance.get_payment_balance()
    assert response == mock_response

def test_topup_service_wallet(api_instance, mocker):
    """Test the topup_service_wallet method."""
    mock_response = {
        "status": "success",
        "message": "Top-up successful"
    }
    mocker.patch('requests.post', return_value=mocker.Mock(status_code=201, json=lambda: mock_response))

    response = api_instance.topup_service_wallet('254700000000', 100)
    assert response == mock_response

def test_initiate_mpesa_stk_push(api_instance, mocker):
    """Test the initiate_mpesa_stk_push method."""
    mock_response = {
        "status": "success",
        "message": "STK Push initiated"
    }
    mocker.patch('requests.post', return_value=mocker.Mock(status_code=201, json=lambda: mock_response))

    response = api_instance.initiate_mpesa_stk_push(100, '254700000000', 'channel_id', 'provider', 'external_reference', 'customer_name', 'callback_url')
    assert response == mock_response

def test_fetch_transactions(api_instance, mocker):
    """Test the fetch_transactions method."""
    mock_response = {
        "transactions": []
    }
    mocker.patch('requests.get', return_value=mocker.Mock(status_code=200, json=lambda: mock_response))

    response = api_instance.fetch_transactions(1, 10)
    assert response == mock_response

def test_fetch_transaction_status(api_instance, mocker):
    """Test the fetch_transaction_status method."""
    mock_response = {
        "status": "completed"
    }
    mocker.patch('requests.get', return_value=mocker.Mock(status_code=200, json=lambda: mock_response))

    response = api_instance.fetch_transaction_status('reference_id')
    assert response == mock_response
