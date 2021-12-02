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


#test1 Позитивные тесты на обновление питомца без фото
@pytest.mark.parametrize("new_name"
    , [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
       special_chars(), '123']
    , ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("new_animal_type"
    , [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
       special_chars(), '123']
    , ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("new_age", ['1'], ids=['min'])
def test_update_pet(new_name, new_animal_type, new_age):
    """Тест на проверку успешного обновления питомца"""

    # Получаем api ключ
    # _, _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список моих питомцев
    _, _, my_pets = pf.get_list_of_pets(pytest.key, "my_pets")

    # Если список не пуст, то обновляем данные первого питомца
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        _, status, result = pf.update_pet(pytest.key, pet_id, new_name, new_animal_type, new_age)

        # Проверяем, что ответ на запрос имеет статус 200 и в тексте имя совпадает с новым именем
        assert status == 200
        assert result['name'] == new_name

    else:
        raise Exception('Нет животных для обновления')


#test2 Позитивные тесты на обновление питомца
@pytest.mark.parametrize("new_name", [''], ids=['empty'])
@pytest.mark.parametrize("new_animal_type", [''], ids=['empty'])
@pytest.mark.parametrize("new_age", ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(),
                                 russian_chars(), russian_chars().upper(), chinese_chars()],
                         ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max', 'int_max + 1',
                              'specials', 'russian', 'RUSSIAN', 'chinese'])
def test_update_pet_negative(new_name, new_animal_type, new_age):
    """Тест на проверку успешного обновления питомца"""

    # Получаем api ключ
    # _, _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список моих питомцев
    _, _, my_pets = pf.get_list_of_pets(pytest.key, "my_pets")

    # Если список не пуст, то обновляем данные первого питомца
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        _, status, result = pf.update_pet(pytest.key, pet_id, new_name, new_animal_type, new_age)

        assert status == 400
    else:
        raise Exception('Нет животных для обновления')


#test3: Тест на добавление фото питомца
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
def test_add_photo(name, animal_type, age, pet_photo):
    """Тест на проверку успешного добавления фото питомца"""

    # Получаем api ключ
    # _, _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список моих питомцев
    _, _, my_pets = pf.get_list_of_pets(pytest.key, "my_pets")

    # Если список пуст, то добавляем нового питомца
    if len(my_pets['pets']) == 0:
        pf.create_pet_without_photo(pytest.key, name, animal_type, age)
        _, _, my_pets = pf.get_list_of_pets(pytest.key, "my_pets")

    # Запоминаем id первого питомца
    pet_id = my_pets['pets'][0]['id']

    # Преобразовываем адрес, по которому лежит фото питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Отправляем запрос на добавление фото питомца
    _, status, result = pf.add_pet_photo(pytest.key, pet_id, pet_photo)

    # Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа есть поле с фото
    assert status == 200
    assert result['pet_photo'] != ""


#test4: Тест на добавление фото питомца
@pytest.mark.parametrize("name", [''], ids=['empty'])
@pytest.mark.parametrize("animal_type", [''], ids=['empty'])
@pytest.mark.parametrize("age", ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(),
                                 russian_chars(), russian_chars().upper(), chinese_chars()],
                         ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max', 'int_max + 1',
                              'specials', 'russian', 'RUSSIAN', 'chinese'])
@pytest.mark.parametrize("pet_photo", ['../images/example.pdf', '../images/broken.jpg'],
                         ids=['pdf', 'broken'])
def test_add_photo_negative(name, animal_type, age, pet_photo):
    """Тест на проверку успешного добавления фото питомца"""

    # Получаем api ключ
    # _, _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список моих питомцев
    _, _, my_pets = pf.get_list_of_pets(pytest.key, "my_pets")

    # Если список пуст, то добавляем нового питомца
    if len(my_pets['pets']) == 0:
        pf.create_pet_without_photo(pytest.key, name, animal_type, age)
        _, _, my_pets = pf.get_list_of_pets(pytest.key, "my_pets")

    # Запоминаем id первого питомца
    pet_id = my_pets['pets'][0]['id']

    # Преобразовываем адрес, по которому лежит фото питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Отправляем запрос на добавление фото питомца
    _, status, result = pf.add_pet_photo(pytest.key, pet_id, pet_photo)

    assert status == 400