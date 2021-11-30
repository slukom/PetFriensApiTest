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


# test1: Позитивные тесты на создание питомца с фото
@pytest.mark.parametrize("name"
    , [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
       special_chars(), '123']
    , ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("animal_type"
    , [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
       special_chars(), '123']
    , ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("age", ['1'], ids=['min'])
@pytest.mark.parametrize("pet_photo", ['../images/cat.jpeg', '../images/cat.png'], ids=['jpeg', 'png'])
def test_add_new_pet_with_photo(name, animal_type, age, pet_photo):
    """Тест на проверку успешного создания питомца с фото в формате jpeg"""

    # Получаем api ключ
    # _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Преобразовываем адрес, по которому лежит фото питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Отправляем запрос на создание нового питомца с фото
    _, status, result = pf.add_new_pet(pytest.key, name, animal_type, age, pet_photo)

    # Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа содержится имя питомца
    assert status == 200
    assert result['name'] == name


# test2: Негативные тесты на создание питомца с фото
@pytest.mark.parametrize("name", [''], ids=['empty'])
@pytest.mark.parametrize("animal_type", [''], ids=['empty'])
@pytest.mark.parametrize("age", ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(),
                                 russian_chars(), russian_chars().upper(), chinese_chars()],
                         ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max', 'int_max + 1',
                              'specials', 'russian', 'RUSSIAN', 'chinese'])
@pytest.mark.parametrize("pet_photo", ['../images/example.pdf', '../images/broken.jpg'],
                         ids=['pdf', 'broken'])
def test_add_new_pet_with_photo_negative(name, animal_type, age, pet_photo):
    """Тест на проверку успешного создания питомца с фото в формате jpeg"""

    # Получаем api ключ
    # _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Преобразовываем адрес, по которому лежит фото питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Отправляем запрос на создание нового питомца с фото
    _, status, result = pf.add_new_pet(pytest.key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


# test3: Позитивные тесты на создание питомца без фото
@pytest.mark.parametrize("name"
    , [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
       special_chars(), '123']
    , ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("animal_type"
    , [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
       special_chars(), '123']
    , ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("age", ['1'], ids=['min'])
def test_successful_create_new_pet_without_photo(name, animal_type, age):
    """Тест на проверку успешного создания питомца без фото"""

    # Получаем api ключ
    # _, _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Отправляем запрос на создание нового питомца с фото
    _, status, result = pf.create_pet_without_photo(pytest.key, name, animal_type, age)

    # Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа содержится имя питомца
    assert status == 200
    assert result['name'] == name


# test4: Негативные тесты на создание питомца без фото
@pytest.mark.parametrize("name", [''], ids=['empty'])
@pytest.mark.parametrize("animal_type", [''], ids=['empty'])
@pytest.mark.parametrize("age",
                         ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(), russian_chars(),
                          russian_chars().upper(), chinese_chars()]
    , ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max', 'int_max + 1', 'specials',
           'russian', 'RUSSIAN', 'chinese'])
def test_create_new_pet_without_photo_pets_negative(name, animal_type, age):
    """Тест на проверку успешного создания питомца без фото"""

    # Получаем api ключ
    # _, _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Отправляем запрос на создание нового питомца с фото
    _, status, result = pf.create_pet_without_photo(pytest.key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
