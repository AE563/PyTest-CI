import pytest
import time
from requests import Response

from unittest.mock import Mock, patch

from currency_exchange import currency_exchange


@pytest.fixture(scope="function", autouse=True)
def time_fixture(request):
    start_time = time.time()
    yield
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Test took {execution_time:.4f} seconds to run")


# Позитивные тесты
@patch('currency_exchange.requests.get')
def test_currency_exchange_positive(mock_get):
    # Создаем мок объект для имитации ответа от API
    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.json.return_value = {"base": "USD", "rates": {"EUR": 0.85}}
    mock_get.return_value = response_mock

    # Проверяем успешную конвертацию с USD в EUR с базовой суммой 1
    result = currency_exchange(base='USD', symbols='EUR')
    assert isinstance(result, float)


# Негативные тесты
def test_currency_exchange_negative_base_value_error():
    with pytest.raises(ValueError):
        currency_exchange(base='RUB')  # Некорректный базовый параметр


def test_currency_exchange_negative_symbols_value_error():
    with pytest.raises(ValueError):
        currency_exchange(symbols='RUB')  # Некорректный базовый параметр


def test_currency_exchange_negative_amount_negative_number():
    with pytest.raises(ValueError):
        currency_exchange(amount=-10)  # Отрицательная базовая сумма


def test_currency_exchange_negative_amount_long_number():
    with pytest.raises(ValueError):
        currency_exchange(amount=123456789012345678901)  # Базовая сумма слишком большая


def test_currency_exchange_negative_places_negative_number():
    with pytest.raises(ValueError):
        currency_exchange(places=-1)  # Отрицательное округление


def test_currency_exchange_negative_places_long_number():
    with pytest.raises(ValueError):
        currency_exchange(places=1234567)  # Слишком большое округление


def test_currency_exchange_negative_source_wrong():
    with pytest.raises(ValueError):
        currency_exchange(source='wrong_source')  # Некорректный источник


# Негативный тест для проверки статуса ответа от API
@patch('currency_exchange.requests.get')
def test_currency_exchange_api_status_negative(mock_get):
    # Создаем мок объект для имитации ответа от API с некорректным статусом
    response_mock = Mock(spec=Response)
    response_mock.status_code = 404  # Устанавливаем статус код 404
    mock_get.return_value = response_mock

    # Проверяем, что функция вызовет ValueError с соответствующим сообщением
    with pytest.raises(ValueError, match=r"Invalid response from API: Status code 404"):
        currency_exchange(base='USD', symbols='EUR', amount=100)

    # Проверяем, что запрос к API был выполнен с нужными параметрами
    mock_get.assert_called_once_with(
        'https://api.exchangerate.host/latest',
        params={'base': 'USD', 'symbols': 'EUR', 'amount': 100, 'places': 2, 'source': 'ecb'}
    )
