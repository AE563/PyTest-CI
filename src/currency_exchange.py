import requests


def currency_exchange(base: str = 'USD',
                      symbols: str = 'EUR',
                      amount: float = 1.0,
                      places: int = 2,
                      source: str = 'ecb') -> float:
    """
    Функция, выполняющая конвертации пары валют.

    Args:
        base (str): Базовая валюта. Должен быть одним из ['USD', 'EUR', 'JPY'].
        symbols (str): Конечная валюта. Должен быть одним из ['USD', 'EUR', 'JPY'].
        amount (float): Сумма конвертации.
        places (int): Округление, количество знаков после запятой.
        source (str): Банк, источника данных. Должен быть одним из ['ecb', 'cbr', 'imf'].
            :Возможные значения для параметра `source`(https://api.exchangerate.host/sources):
            - 'ecb': Центральный банк Европы. Нет возможности конвертировать рубли.
            - 'cbr': Центральный Банк России. Не возвращает данные (работает по xml).
            - 'imf': Международный валютный фонд. Все ОК.

    Returns:
        float: Результат конвертации валют

    Raises:
        ValueError: Если параметр `base` или `symbols` не является строкой.
        ValueError: Если параметр `amount` не является числом, меньше или равен нулю, имеет более 20 знаков.
        ValueError: Если параметр `places` не является целым числом, меньше нуля, имеет более 5 знаков.
        ValueError: Если параметр `source` не принадлежит к ['ecb', 'cbr', 'imf'].
        ValueError: Если ответ от API не содержит данные rates или не является числом.

    """
    if not isinstance(base, str):
        raise ValueError("Parameter 'base' must be a string.")
    if base not in ['USD', 'EUR', 'JPY']:
        raise ValueError("Parameter 'base' must be one of ['USD', 'EUR', 'JPY'].")
    if not isinstance(symbols, str):
        raise ValueError("Parameter 'symbols' must be a string.")
    if symbols not in ['USD', 'EUR', 'JPY']:
        raise ValueError("Parameter 'symbols' must be one of ['USD', 'EUR', 'JPY'].")
    if not isinstance(amount, (int, float)):
        raise ValueError("Parameter 'amount' must be a number.")
    if amount <= 0:
        raise ValueError("Parameter 'amount' must be a positive number.")
    if len(str(amount)) > 20:
        raise ValueError("Parameter 'amount' must have at most 20 digits.")
    if not isinstance(places, int):
        raise ValueError("Parameter 'places' must be an integer.")
    if places <= 0:
        raise ValueError("Parameter 'places' must be a positive number.")
    if len(str(places)) > 5:
        raise ValueError("Parameter 'places' must have at most 5 digits.")
    if source not in ['ecb', 'cbr', 'imf']:
        raise ValueError("Parameter 'source' must be one of ['ecb', 'cbr', 'imf'].")

    url = 'https://api.exchangerate.host/latest'
    query_parameters = {'base': base, 'symbols': symbols, 'amount': amount, 'places': places, 'source': source}
    response = requests.get(url, params=query_parameters)

    # Проверка статуса ответа от API
    if response.status_code != 200:
        raise ValueError(f"Invalid response from API: Status code {response.status_code}")

    data = response.json()

    # Проверка ответа от API
    if not data.get('rates') or not isinstance(data['rates'].get(symbols), (int, float)):
        raise ValueError("Invalid response from API: rates not found or not a number.")

    result = data['rates'][symbols]

    return result

