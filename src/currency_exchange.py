import requests


def currency_exchange(base: str = 'USD',
                      symbols: str = 'EUR',
                      amount: float = 1.0,
                      places: int = 2,
                      source: str = 'ecb',
                      url: str = 'https://api.exchangerate.host/latest') -> float:
    """
    Function that performs currency pair conversions.

    Args:
        base (str): Base currency. Must be one of ['USD', 'EUR', 'JPY'].
        symbols (str): Ultimate currency. Must be one of ['USD', 'EUR', 'JPY'].
        amount (float): The conversion amount.
        places (int): Rounding, number of decimal places.
        source (str): Bank, data source. Must be one of ['ecb', 'cbr', 'imf'].
            Possible values for the `source`(https://api.exchangerate.host/sources):
            - 'ecb': Central Bank of Europe. There is no possibility to convert rubles.
            - 'cbr': Central Bank of Russia. Does not return data (works by xml).
            - 'imf': International Monetary Fund. All OK.
        url (str):

    Returns:
        float: Currency conversion result

    Raises:
        ValueError: If the `base` parameter does not belong to ['USD', 'EUR', 'JPY'].
        ValueError: If the `symbols` parameter does not belong to ['USD', 'EUR', 'JPY'].
        ValueError: If the `amount` is not a number.
        ValueError: If the `amount` parameter is less than or equal to zero.
        ValueError: If the `amount` parameter has more than 20 characters.
        ValueError: If the `places` parameter is not an integer less than zero.
        ValueError: If the `places` parameter has more than 5 characters.
        ValueError: If the `source` parameter does not belong to ['ecb', 'cbr', 'imf'].
        ValueError: If the status response code not equal 200.
        ValueError: If the response does not contain rates data or not a number.

    """
    variables_base = ['USD', 'EUR', 'JPY']
    variables_symbols = ['USD', 'EUR', 'JPY']
    max_number_amount_length = 20
    max_number_decimal_places = 5
    variables_source = ['ecb', 'cbr', 'imf']

    if base not in variables_base:
        raise ValueError(f"Parameter 'base' must be one of {variables_base}. "
                         f"You enter: '{base}'")
    if symbols not in variables_symbols:
        raise ValueError(f"Parameter 'symbols' must be one of {variables_symbols}. "
                         f"You enter: '{symbols}'")
    if not isinstance(amount, (int, float)):
        raise ValueError(f"Parameter 'amount' must be a number. "
                         f"You use: '{type(amount)}'")
    if amount <= 0:
        raise ValueError(f"Parameter 'amount' must be a positive number. "
                         f"You enter: {amount}")
    if len(str(amount)) > max_number_amount_length:
        raise ValueError(f"Parameter 'amount' must have at most 20 digits. "
                         f"You enter: {len(str(amount))}")
    if not isinstance(places, int):
        raise ValueError(f"Parameter 'places' must be an integer. "
                         f"You use: '{type(places)}'")
    if places < 0:
        raise ValueError(f"Parameter 'places' must be a positive number ore zero. "
                         f"You enter: '{places}'")
    if len(str(places)) > max_number_decimal_places:
        raise ValueError(f"Parameter 'places' must have at most 5 digits. "
                         f"You enter: {len(str(places))}")
    if source not in variables_source:
        raise ValueError(f"Parameter 'source' must be one of {variables_source}. "
                         f"You enter: '{source}'")

    query_parameters = {'base': base,
                        'symbols': symbols,
                        'amount': amount,
                        'places': places,
                        'source': source}
    response = requests.get(url, params=query_parameters)

    # Checking the response status from the API
    if response.status_code != 200:
        raise ValueError(f"Invalid API response: Status code: {response.status_code}")

    data = response.json()

    # Checking the response from the API
    if not data.get('rates') or \
            not isinstance(data['rates'].get(symbols), (int, float)):
        raise ValueError(f"Invalid response from API: rates not found or not number."
                         f"Response is: {data['rates'].get(symbols)}")

    result = data['rates'][symbols]

    return result
