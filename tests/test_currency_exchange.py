import os
import pytest
import docker

from config import mock_config_path
from src.currency_exchange import currency_exchange, ERROR_MESSAGES


@pytest.fixture(scope="module")
def docker_container():
    if os.environ.get('GITHUB_ACTIONS') != 'true':
        client = docker.from_env()
        container = client.containers.run("jordimartin/mmock",
                                          detach=True,
                                          volumes={mock_config_path: {'bind': '/config', 'mode': 'rw'}},
                                          ports={'8082': 8082, '8083': 8083})

        yield container

        container.stop()
        container.remove()
    else:
        yield None


# Positive tests
# def test_currency_exchange_positive():
#     return True


# Negative tests
def test_currency_exchange_negative_base_value_error():
    with pytest.raises(ValueError) as excinfo:
        currency_exchange(base='RUB')  # Invalid base parameter

    expected_error_message = ERROR_MESSAGES["base_value"]
    assert str(excinfo.value) == expected_error_message


def test_currency_exchange_negative_symbols_value_error():
    with pytest.raises(ValueError) as excinfo:
        currency_exchange(symbols='RUB')  # Invalid base parameter

    expected_error_message = ERROR_MESSAGES["symbols_value"]
    assert str(excinfo.value) == expected_error_message


def test_currency_exchange_negative_amount_negative_number():
    with pytest.raises(ValueError) as excinfo:
        currency_exchange(amount=-10)  # Negative base amount

    expected_error_message = ERROR_MESSAGES["amount_positive"]
    assert str(excinfo.value) == expected_error_message


def test_currency_exchange_negative_amount_long_number():
    with pytest.raises(ValueError) as excinfo:
        currency_exchange(amount=123456789012345678901)  # The base amount is too high

    expected_error_message = ERROR_MESSAGES["amount_length"]
    assert str(excinfo.value) == expected_error_message


def test_currency_exchange_negative_places_negative_number():
    with pytest.raises(ValueError) as excinfo:
        currency_exchange(places=-1)  # Negative rounding

    expected_error_message = ERROR_MESSAGES["places_positive"]
    assert str(excinfo.value) == expected_error_message


def test_currency_exchange_negative_places_long_number():
    with pytest.raises(ValueError) as excinfo:
        currency_exchange(places=1234567)  # Too much rounding

    expected_error_message = ERROR_MESSAGES["places_length"]
    assert str(excinfo.value) == expected_error_message


def test_currency_exchange_negative_source_wrong():
    with pytest.raises(ValueError) as excinfo:
        currency_exchange(source='wrong_source')  # Incorrect Source

    expected_error_message = ERROR_MESSAGES["source_value"]
    assert str(excinfo.value) == expected_error_message


# Negative test to check the response status from the API
def test_currency_exchange_api_status_negative(docker_container):
    with pytest.raises(ValueError) as excinfo:
        currency_exchange()

    expected_prefix = "Invalid response from API: Status code "
    assert str(excinfo.value).startswith(expected_prefix)
