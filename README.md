[![CI](https://github.com/AE563/PyTest-CI/actions/workflows/ci.yml/badge.svg)](https://github.com/AE563/PyTest-CI/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/AE563/PyTest-CI/branch/main/graph/badge.svg?token=6WH63OWSW2)](https://codecov.io/gh/AE563/PyTest-CI)
[![CI](https://github.com/AE563/PyTest-CI/actions/workflows/ci.yml/badge.svg?event=deployment_status)](https://github.com/AE563/PyTest-CI/actions/workflows/ci.yml)

- [Function Description](#function-description)
- [Test Cases](#test-cases)
- [Docker Setup for Testing](#docker-setup-for-testing)
- [Mocking API Responses](#mocking-api-responses)
- [Continuous Integration / Continuous Deployment (CI/CD)](#continuous-integration--continuous-deployment-cicd)
- [Linter](#linter)
- [Running Tests](#running-tests)

# Currency Exchange Function and Tests

This repository contains a Python function `currency_exchange` that performs currency pair conversions. It also includes positive and negative test cases for the function. This work was completed as part of a test assignment for a job interview.

## Function Description

The `currency_exchange` function takes the following parameters:

- `base` (str): Base currency. Possible values are 'USD', 'EUR', 'JPY' (default: 'USD').
- `symbols` (str): Ultimate currency. Possible values are 'USD', 'EUR', 'JPY' (default: 'EUR').
- `amount` (float): The conversion amount (default: 1.0).
- `places` (int): Rounding, number of decimal places (default: 2).
- `source` (str): Data source for exchange rates. Possible values are 'ecb', 'cbr', 'imf' (default: 'ecb').
- `url` (str): API URL argument added separately for ease of testing (default: 'https://api.exchangerate.host/latest').

The function returns the result of currency conversion as a float.

It raises various `ValueError` exceptions for invalid input parameters, such as incorrect base or symbols, non-numeric amount, incorrect source, and more. See the function's docstring for a full list of raised exceptions.

## Test Cases

The test cases are divided into positive and negative scenarios and are implemented using the `pytest` testing framework. The positive tests check the correct behavior of the function under valid conditions, while the negative tests verify that the function raises appropriate exceptions for invalid inputs.

### Positive Tests

- `test_currency_exchange_positive`: Tests the currency conversion function with valid inputs and checks if the result matches the expected value.

### Negative Tests

- `test_currency_exchange_negative_base_value_error`: Tests that the function raises an error when an invalid base parameter is provided.
- `test_currency_exchange_negative_symbols_value_error`: Tests that the function raises an error when an invalid symbols parameter is provided.
- ... (similarly for other negative test cases)

### Integration Test

- `test_currency_exchange_api_status_negative`: Tests that the function handles invalid API responses appropriately.

## Docker Setup for Testing

The project uses Docker to set up a consistent testing environment. A Docker container is created using the `jordimartin/mmock` image for mocking API responses. The `docker_container` fixture in the tests sets up this container, ensuring reliable and isolated testing.

## Mocking API Responses

To simulate different API responses during testing, the function uses the `unittest.mock` library to mock the behavior of external APIs. This allows controlled testing of various scenarios without making actual API requests.

## Continuous Integration / Continuous Deployment (CI/CD)

This project has been integrated into a CI/CD pipeline to automate testing using GitHub Actions. Whenever changes are pushed to the repository, GitHub Actions automatically triggers the test suite to ensure that code changes are thoroughly tested before they are merged into the main branch.

The CI/CD pipeline performs the following steps:

1. **Testing**: When code changes are pushed to the repository, GitHub Actions runs the test suite using the `pytest` framework. This ensures that both positive and negative test cases are executed to validate the correctness of the function.

2. **Docker Setup**: As part of the testing process, a Docker container is set up using the `jordimartin/mmock` image. This container is used to mock API responses and isolate the testing environment.

3. **Mocking API Responses**: The function's behavior is tested under various scenarios by using the [Mmock(aka Monsters Mock)](https://github.com/jmartin82/mmock) library to mock the behavior of external APIs. This allows controlled testing without making actual API requests.

4. **Code Coverage**: Test coverage analysis is integrated into the pipeline to measure the percentage of code covered by tests. This provides insights into which parts of the codebase are thoroughly tested and identifies areas that may require additional testing.

5. **Results and Reporting**: The test results and code coverage information are reported back to GitHub. You can easily view the testing status, coverage percentage, and detailed coverage reports for each commit or pull request.

6. **Deployment to Server**: Upon successful testing, the code can be automatically deployed to a production or staging server. This ensures that only tested and verified code reaches the deployment environment.

By automating the testing process, integrating code coverage analysis, and incorporating deployment steps, this project ensures that the currency exchange function is thoroughly tested, validated, and seamlessly deployed. This contributes to maintaining the reliability and stability of the codebase while optimizing the development workflow.

## Linter
The project also includes code checking with Flake8, a popular linter for Python. Running code checking with Flake8 allows you to keep track of style standards and detect potential bugs.

To run the Flake8 linter, make sure you have the required dependencies installed, then execute:

```bash
flake8
```

## Running Tests

To run the tests, you need to have Python and the pytest library installed. Here's how you can set up the environment and run the tests:

1. **Python Installation (Ubuntu)**: If you don't have Python installed, you can install it using the package manager. Open your terminal and run the following commands:

    ```bash
    sudo apt update
    sudo apt install python3
    ```

2. **Environment Setup**:
    - Clone the repository to your local machine.
    ```bash
    git clone git@github.com:AE563/PyTest-CI.git
    ```
    - Navigate to the project directory using the terminal.

3. **Install Dependencies**: The project may have dependencies listed in the `requirements.txt` file. You can install them using the following command:

    ```bash
    pip install -r requirements.txt
    ```

4. **Running Tests**: Execute the following command in the terminal:

    ```bash
    pytest
    ```

The tests will execute, and the results will be displayed in the terminal. This ensures that the function's behavior is thoroughly tested, and any issues are identified before merging the code into the main branch.

By following these steps, you can confidently test the currency exchange function and ensure its reliability and correctness.

---

This project demonstrates the implementation of a currency exchange function and its associated tests. It showcases coding skills, testing practices, and handling of API responses in a real-world scenario, Docker, Mock, CI/CD.
