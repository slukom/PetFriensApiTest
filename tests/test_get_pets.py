from api import PetFriends
from settings import valid_email, valid_password
import os
import pytest

pf = PetFriends()


def is_age_valid(age):
    # Проверяем, что возраст - это число от 1 до 49 и целое
    return age.isdigit() and 0 < int(age) < 50 and float(age) == int(age)


def generate_string(num):
    return "x" * num


def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'


def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'


@pytest.fixture(autouse=True)
def get_api_key():
    # """ Проверяем, что запрос api-ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    _, status, pytest.key = pf.get_api_key(valid_email, valid_password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in pytest.key

    yield


# test1: Позитивные тесты на получение списка питомцев
@pytest.mark.parametrize('filter', ['', 'my_pets'], ids=['empty', 'mypets'])
def test_get_pets(filter):
    """Тест на проверку получения списка всех питомцев"""

    # Отправляем запрос на получение списка всех питомцев
    _, status, result = pf.get_list_of_pets(pytest.key, filter)

    # Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа содержится список питомцев
    assert status == 200
    assert len(result['pets']) > 0


# test2: Негативные тесты на получение списка питомцев
@pytest.mark.parametrize('filter'
    , ['dog', generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
       special_chars(), '123']
    , ids=['dog', '255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
def test_get_pets_negative(filter):
    """Тест на проверку получения списка всех питомцев"""

    # Отправляем запрос на получение списка всех питомцев
    _, status, result = pf.get_list_of_pets(pytest.key, filter)

    assert status == 400


# test 3: Негативные тесты на получение списка питомцев с
@pytest.mark.parametrize('auth_key'
    , ['', generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
       special_chars(), '123']
    , ids=['empty', '255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize('filter', ['', 'my_pets'], ids=['empty', 'mypets'])
def test_get_all_pets_with_incorrect_auth_key(auth_key, filter):
    """Тест на проверку получения списка питомцев с некорректным api ключом"""

    # Создаем пустой ключ
    auth_key = {'key': ''}

    # Отправляем запрос на получение списка всех питомцев
    _, status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем, что ответ на запрос имеет статус 403
    assert status == 403
