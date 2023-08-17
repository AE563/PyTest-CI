import requests


def currency_exchange(base: str = 'USD',
                      symbols: str = 'EUR',
                      amount: float = 1.0,
                      places: int = 2,
                      source: str = 'ecb') -> float:
    """
    Function that performs currency pair conversions.

    Args:
        base (str): Base currency. Must be one of ['USD', 'EUR', 'JPY'].
        symbols (str): Ultimate currency. Must be one of ['USD', 'EUR', 'JPY'].
        amount (float): The conversion amount.
        places (int): Rounding, number of decimal places.
        source (str): Bank, data source. Must be one of ['ecb', 'cbr', 'imf'].
            :Possible values for the `source`(https://api.exchangerate.host/sources) parameter:
            - 'ecb': Central Bank of Europe. There is no possibility to convert rubles.
            - 'cbr': Central Bank of Russia. Does not return data (works by xml).
            - 'imf': International Monetary Fund. All OK.

    Returns:
        float: Currency conversion result

    Raises:
        ValueError: If the `base` or `symbols` parameter is not a string.
        ValueError: If the `base` parameter does not belong to ['USD', 'EUR', 'JPY'].
        ValueError: If the parameter `symbols` or `symbols` is not a string.
        ValueError: If the `symbols` parameter does not belong to ['USD', 'EUR', 'JPY'].
        ValueError: If the parameter `amount` is not a number, is less than or equal to zero, has more than 20 characters.
        ValueError: If the `amount` parameter is less than or equal to zero.
        ValueError: If the `amount` parameter has more than 20 characters.
        ValueError: If the `places` parameter is not an integer less than zero.
        ValueError: If the `places` parameter has more than 5 characters.
        ValueError: If the ``source` parameter does not belong to ['ecb', 'cbr', 'imf'].
        ValueError: If the response from the API does not contain rates data or is not a number.

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

    # Checking the response status from the API
    if response.status_code != 200:
        raise ValueError(f"Invalid response from API: Status code {response.status_code}")

    data = response.json()

    # Checking the response from the API
    if not data.get('rates') or not isinstance(data['rates'].get(symbols), (int, float)):
        raise ValueError("Invalid response from API: rates not found or not a number.")

    result = data['rates'][symbols]

    return result

