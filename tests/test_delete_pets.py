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


#test1: Позитивный тест на удаление питомца
def test_delete_pet():
    """Тест на проверку успешного удаления питомца"""

    # Получаем api ключ
    # _, _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список моих питомцев
    _, _, my_pets = pf.get_list_of_pets(pytest.key, "my_pets")

    # Если список пуст, то добавляем нового питомца
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(pytest.key, "Пушок", "cat", "3", "../images/cat.jpeg")
        _, _, my_pets = pf.get_list_of_pets(pytest.key, "my_pets")

    # Запоминаем id первого питомца
    pet_id = my_pets['pets'][0]['id']

    # Отправляем запрос на удаление питомца
    _, status, result = pf.delete_pet(pytest.key, pet_id)

    # Снова получаем список моих питомцев
    _, _, my_pets = pf.get_list_of_pets(pytest.key, "my_pets")

    # Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа нет id удаленного питомца
    assert status == 200
    assert pet_id not in my_pets


#test2: Негативные тесты на удаление питомца
@pytest.mark.parametrize('pet_id'
    , ['', generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
       special_chars(), '123']
    , ids=['empty', '255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
def test_delete_pet_negative(pet_id):
    """Тест на проверку удаления несуществующего питомца"""

    # Отправляем запрос на удаление питомца
    _, status, result = pf.delete_pet(pytest.key, pet_id)

    assert status == 404