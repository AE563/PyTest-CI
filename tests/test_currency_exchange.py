import pytest
import time
from requests import Response

from unittest.mock import Mock, patch

from src.currency_exchange import currency_exchange


@pytest.fixture(scope="function", autouse=True)
def time_fixture(request):
    start_time = time.time()
    yield
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Test took {execution_time:.4f} seconds to run")


# Positive tests
@patch('src.currency_exchange.requests.get')
def test_currency_exchange_positive(mock_get):
    # Create a mock object to simulate a response from the API
    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.json.return_value = {"base": "USD", "rates": {"EUR": 0.85}}
    mock_get.return_value = response_mock

    # Check successful conversion from USD to EUR with base amount 1
    result = currency_exchange(base='USD', symbols='EUR')
    assert isinstance(result, float)


# Negative tests
def test_currency_exchange_negative_base_value_error():
    with pytest.raises(ValueError):
        currency_exchange(base='RUB')  # Invalid base parameter


def test_currency_exchange_negative_symbols_value_error():
    with pytest.raises(ValueError):
        currency_exchange(symbols='RUB')  # Invalid base parameter


def test_currency_exchange_negative_amount_negative_number():
    with pytest.raises(ValueError):
        currency_exchange(amount=-10)  # Negative base amount


def test_currency_exchange_negative_amount_long_number():
    with pytest.raises(ValueError):
        currency_exchange(amount=123456789012345678901)  # The base amount is too high


def test_currency_exchange_negative_places_negative_number():
    with pytest.raises(ValueError):
        currency_exchange(places=-1)  # Negative rounding


def test_currency_exchange_negative_places_long_number():
    with pytest.raises(ValueError):
        currency_exchange(places=1234567)  # Too much rounding


def test_currency_exchange_negative_source_wrong():
    with pytest.raises(ValueError):
        currency_exchange(source='wrong_source')  # Incorrect Source


# Negative test to check the response status from the API
def test_currency_exchange_api_status_negative():
    print(currency_exchange())
    return


@patch('src.currency_exchange.requests.get')
def test_currency_exchange_api_status_mock_negative(mock_get):
    # Create a mock object to simulate a response from API with an incorrect status
    response_mock = Mock(spec=Response)
    response_mock.status_code = 404  # Set status code 404
    mock_get.return_value = response_mock

    # Check that the function will call ValueError with the corresponding message
    with pytest.raises(ValueError, match=r"Invalid response from API: Status code 404"):
        currency_exchange(base='USD', symbols='EUR', amount=100)

    # Check that the API request has been executed with the required parameters
    mock_get.assert_called_once_with(
        'https://api.exchangerate.host/latest',
        params={'base': 'USD', 'symbols': 'EUR', 'amount': 100, 'places': 2, 'source': 'ecb'}
    )
