>[!@pytest.mark.parametrize]-
>Параметризует тестовую функцию, позволяя запускать ее с разными наборами параметров.
>```python
>import pytest
>
>@pytest.mark.parametrize("input, expected", [(1, 2), (2, 4), (3, 6)])
>def test_multiply_by_two(input, expected):
>    result = input * 2
>    assert result == expected
>
>```

>[!@pytest.mark.parametrize (с параметром `ids`)]-
>Параметризует тесты с возможностью задать идентификаторы для каждого набора параметров.
>```python
>import pytest
>@pytest.mark.parametrize("input, expected", [(1, 2), (2, 4), (3, 6)], ids=["case1", "case2", "case3"])
>def test_multiply_by_two(input, expected):
>    result = input * 2
>    assert result == expected
>```

>[!@pytest.mark.parametrize (с параметром `indirect=True`)]-
>Позволяет передать фикстуру в качестве аргумента для параметризованного теста.
>```python
>import pytest
>@pytest.fixture
>def multiplier(request):
>    return request.param * 2
>
>@pytest.mark.parametrize("multiplier", [1, 2, 3], indirect=True)
>def test_multiply_by_param(multiplier):
>	result = 5 * multiplier
>	assert result % 2 == 0
>```
____

>[!@pytest.mark.skip` и `@pytest.mark.skipif]-
>`@pytest.mark.skip`- позволяет пропустить выполнение тестов, 
>```python
>import pytest
>
>@pytest.mark.skip(reason="Test is not ready yet")
>def test_my_feature():
>	# ...
>```
>`@pytest.mark.skipif` -  позволяет пропустить тест на основе условия.
>```python
>import pytest
>import sys
>@pytest.mark.skipif(sys.version_info < (3, 7), reason="Requires Python 3.7 or higher")
>def test_new_feature():
>    # Тесты для новой функциональности, требующей Python 3.7+
>    pass
>```

>[!@pytest.mark.xfail]-
>Помечает тест как "ожидаемо неудачный", результат неуспешного теста не считается ошибкой.
>```python
>import pytest
>23
>@pytest.mark.xfail
>def test_divide_by_zero():
>    result = 5 / 0
>    assert result == float("inf")
>```

>[!@pytest.mark.timeout]-
>Устанавливает ограничение времени выполнения теста.
>```python
>import pytest
>import time
>@pytest.mark.timeout(5)  # Тест должен завершиться за 5 секунд
>def test_long_running_task():
>    time.sleep(10)
>```

>[!@pytest.mark.usefixtures]-
>Позволяет использовать фикстуры в тестовых функциях без явной передачи в аргументах.
>```python
>import pytest
>
>@pytest.fixture
>def my_fixture():
>    return "Hello, pytest!"
>
>@pytest.mark.usefixtures("my_fixture")
>def test_using_fixture():
>    # my_fixture будет автоматически передана в этот тест
>    assert my_fixture == "Hello, pytest!"
>```

>[!@pytest.mark.dependency]-
>Позволяет определить зависимости между тестами, контролируя порядок их выполнения.
>```python
>import pytest
>@pytest.mark.dependency
>def test_first():
>    pass
>
>@pytest.mark.dependency(depends=["test_first"])
>def test_second():
>    pass
>```
____

>[!@pytest.fixture]-
>Создает фикстуры - функции, предоставляющие предварительные условия для тестов или общие ресурсы.
>```python
>import pytest
>
>@pytest.fixture
>def my_fixture():
>    return "Hello, pytest!"
>
>def test_using_fixture(my_fixture):
>    assert my_fixture == "Hello, pytest!"
>```

>[!@pytest.fixture(autouse=True)]-
>```python
>import pytest
>
>@pytest.fixture(autouse=True)
>def setup_and_teardown():
>    print("Setup before test")  # Это будет выполнено перед каждым тестом
>    yield  # Здесь происходит выполнение тестовой функции
>    print("Teardown after test")  # Это будет выполнено после каждого теста
>
>def test_example_1():
>    assert 1 + 1 == 2
>```
