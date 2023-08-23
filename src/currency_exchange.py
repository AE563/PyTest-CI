import requests
from config import DEBUG


ERROR_MESSAGES = {
    "base_string": "Parameter 'base' must be a string.",
    "base_value": "Parameter 'base' must be one of ['USD', 'EUR', 'JPY'].",
    "symbols_string": "Parameter 'symbols' must be a string.",
    "symbols_value": "Parameter 'symbols' must be one of ['USD', 'EUR', 'JPY'].",
    "amount_type": "Parameter 'amount' must be a number.",
    "amount_positive": "Parameter 'amount' must be a positive number.",
    "amount_length": "Parameter 'amount' must have at most 20 digits.",
    "places_type": "Parameter 'places' must be an integer.",
    "places_positive": "Parameter 'places' must be a positive number.",
    "places_length": "Parameter 'places' must have at most 5 digits.",
    "source_value": "Parameter 'source' must be one of ['ecb', 'cbr', 'imf'].",
    "invalid_api_response": "Invalid response from API: rates not found or not a number.",
}


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
            Possible values for the `source`(https://api.exchangerate.host/sources) parameter:
            - 'ecb': Central Bank of Europe. There is no possibility to convert rubles.
            - 'cbr': Central Bank of Russia. Does not return data (works by xml).
            - 'imf': International Monetary Fund. All OK.

    Returns:
        float: Currency conversion result

    Raises:
        ValueError: If the `base` or `symbols` parameter is not a string.
        ValueError: If the `base` parameter does not belong to ['USD', 'EUR', 'JPY'].
        ValueError: If the `symbols` is not a string.
        ValueError: If the `symbols` parameter does not belong to ['USD', 'EUR', 'JPY'].
        ValueError: If the `amount` is not a number, is less than or equal to zero, has more than 20 characters.
        ValueError: If the `amount` parameter is less than or equal to zero.
        ValueError: If the `amount` parameter has more than 20 characters.
        ValueError: If the `places` parameter is not an integer less than zero.
        ValueError: If the `places` parameter has more than 5 characters.
        ValueError: If the `source` parameter does not belong to ['ecb', 'cbr', 'imf'].
        ValueError: If the response from the API does not contain rates data or is not a number.

    """

    if base not in ['USD', 'EUR', 'JPY']:
        raise ValueError(ERROR_MESSAGES["base_value"])
    if not isinstance(symbols, str):
        raise ValueError(ERROR_MESSAGES["symbols_string"])
    if symbols not in ['USD', 'EUR', 'JPY']:
        raise ValueError(ERROR_MESSAGES["symbols_value"])
    if not isinstance(amount, (int, float)):
        raise ValueError(ERROR_MESSAGES["amount_type"])
    if amount <= 0:
        raise ValueError(ERROR_MESSAGES["amount_positive"])
    if len(str(amount)) > 20:
        raise ValueError(ERROR_MESSAGES["amount_length"])
    if not isinstance(places, int):
        raise ValueError(ERROR_MESSAGES["places_type"])
    if places <= 0:
        raise ValueError(ERROR_MESSAGES["places_positive"])
    if len(str(places)) > 5:
        raise ValueError(ERROR_MESSAGES["places_length"])
    if source not in ['ecb', 'cbr', 'imf']:
        raise ValueError(ERROR_MESSAGES["source_value"])

    url = 'https://api.exchangerate.host/latest'
    # Mock url for test's
    if DEBUG is True:
        url = 'http://0.0.0.0:8083/status-code404'

    query_parameters = {'base': base, 'symbols': symbols, 'amount': amount, 'places': places, 'source': source}
    response = requests.get(url, params=query_parameters)

    # Checking the response status from the API
    if response.status_code != 200:
        raise ValueError(f"Invalid response from API: Status code {response.status_code}")

    data = response.json()

    # Checking the response from the API
    if not data.get('rates') or not isinstance(data['rates'].get(symbols), (int, float)):
        raise ValueError(ERROR_MESSAGES["invalid_api_response"])

    result = data['rates'][symbols]

    return result
