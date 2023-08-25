import os
import pytest
import docker

from config import mock_conf_path
from src.currency_exchange import currency_exchange


@pytest.fixture(scope="module")
def docker_container():
    """
    Fixture for setting up a Docker container for testing.

    This fixture is used to create a Docker container for testing purposes.
    It checks if the code is running in a GitHub Actions environment. If not,
    it creates and sets up a Docker container using the specified image and parameters.
    After the test, the container is stopped and removed.
    """
    if os.environ.get('GITHUB_ACTIONS') != 'true':
        client = docker.from_env()
        container = client.containers.run("jordimartin/mmock",
                                          detach=True,
                                          volumes={mock_conf_path: {'bind': '/config'}},
                                          ports={'8082': 8082, '8083': 8083})

        yield container

        container.stop()
        container.remove()
    else:
        yield None


# Positive tests
def test_currency_exchange_positive(docker_container):
    expected_result = 0.92
    result = currency_exchange(url='http://0.0.0.0:8083/latest')
    assert result == expected_result, f"Expected {expected_result}, but got {result}"


# Negative tests
def test_currency_exchange_negative_base_value_error():
    with pytest.raises(ValueError) as excinfo:
        currency_exchange(base='RUB')  # Invalid base parameter

    expected_prefix = "Parameter 'base' must be one of ['USD', 'EUR', 'JPY']."
    assert str(excinfo.value).startswith(expected_prefix)


def test_currency_exchange_negative_symbols_value_error():
    with pytest.raises(ValueError) as excinfo:
        currency_exchange(symbols='RUB')  # Invalid base parameter

    expected_prefix = "Parameter 'symbols' must be one of ['USD', 'EUR', 'JPY']."
    assert str(excinfo.value).startswith(expected_prefix)


def test_currency_exchange_negative_amount_negative_number():
    with pytest.raises(ValueError) as excinfo:
        currency_exchange(amount=-10)  # Negative base amount

    expected_prefix = "Parameter 'amount' must be a positive number."
    assert str(excinfo.value).startswith(expected_prefix)


def test_currency_exchange_negative_amount_long_number():
    with pytest.raises(ValueError) as excinfo:
        currency_exchange(amount=123456789012345678901)  # The base amount is too high

    expected_prefix = "Parameter 'amount' must have at most 20 digits."
    assert str(excinfo.value).startswith(expected_prefix)


def test_currency_exchange_negative_places_negative_number():
    with pytest.raises(ValueError) as excinfo:
        currency_exchange(places=-1)  # Negative rounding

    expected_prefix = "Parameter 'places' must be a positive number ore zero."
    assert str(excinfo.value).startswith(expected_prefix)


def test_currency_exchange_negative_places_long_number():
    with pytest.raises(ValueError) as excinfo:
        currency_exchange(places=1234567)  # Too much rounding

    expected_prefix = "Parameter 'places' must have at most 5 digits."
    assert str(excinfo.value).startswith(expected_prefix)


def test_currency_exchange_negative_source_wrong():
    with pytest.raises(ValueError) as excinfo:
        currency_exchange(source='wrong_source')  # Incorrect Source

    expected_prefix = "Parameter 'source' must be one of ['ecb', 'cbr', 'imf']."
    assert str(excinfo.value).startswith(expected_prefix)


# Negative test to check the response status from the API
def test_currency_exchange_api_status_negative(docker_container):
    with pytest.raises(ValueError) as excinfo:
        currency_exchange(url='http://0.0.0.0:8083/status-code404')

    expected_prefix = "Invalid API response: Status code: "
    assert str(excinfo.value).startswith(expected_prefix)
