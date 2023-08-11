import pytest
from requests import Response

from unittest.mock import Mock, patch

from src.currency_exchange import currency_exchange


# Позитивные тесты
def test_currency_exchange_positive():
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
def test_currency_exchange_api_status_negative():
    # Создаем мок объект для имитации ответа от API с некорректным статусом
    response_mock = Mock(spec=Response)
    response_mock.status_code = 404  # Устанавливаем статус код 404

    # Имитируем запрос к API с помощью патча
    with patch('requests.get', return_value=response_mock) as mock_request:
        # Проверяем, что функция вызовет ValueError с соответствующим сообщением
        with pytest.raises(ValueError, match=r"Invalid response from API: Status code 404"):
            currency_exchange(base='USD', symbols='EUR', amount=100)

        # Проверяем, что запрос к API был выполнен с нужными параметрами
        mock_request.assert_called_once_with(
            'https://api.exchangerate.host/latest',
            params={'base': 'USD', 'symbols': 'EUR', 'amount': 100, 'places': 2, 'source': 'ecb'}
        )
