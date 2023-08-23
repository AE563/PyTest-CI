import os
import pytest
import docker

from config import mock_config_path
from src.currency_exchange import currency_exchange


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
def test_currency_exchange_positive():
    return True


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
def test_currency_exchange_api_status_negative(docker_container):
    with pytest.raises(ValueError):
        currency_exchange()
    return
