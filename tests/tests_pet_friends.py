from api import PetFriends
from settings import valid_email, valid_password
import os
import pytest

pf = PetFriends()


@pytest.fixture()
def get_key():
    _, status, key = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert 'key' in key
    return key


# test 1
@pytest.mark.positive
@pytest.mark.api
@pytest.mark.auth
# @pytest.mark.skip(reason="Не использует фикстуру get_key")
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Тест на проверку получения api ключа"""

    # Отправляем запрос на получение api ключа
    _, status, result = pf.get_api_key(email, password)

    #  Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа содержится поле 'key'
    assert status == 200
    assert 'key' in result


# test 2
@pytest.mark.positive
@pytest.mark.api
@pytest.mark.get
def test_get_all_pets_with_valid_key(get_key, filter=''):
    """Тест на проверку получения списка всех питомцев"""

    # Получаем api ключ
    # _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Отправляем запрос на получение списка всех питомцев
    _, status, result = pf.get_list_of_pets(get_key, filter)

    # Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа содержится список питомцев
    assert status == 200
    assert len(result['pets']) > 0


# test 3
@pytest.mark.positive
@pytest.mark.api
@pytest.mark.create
def test_add_new_pet_with_valid_data_jpeg(get_key, name='Барсик', animal_type='cat', age='2',
                                          pet_photo='../images/cat.jpeg'):
    """Тест на проверку успешного создания питомца с фото в формате jpeg"""

    # Получаем api ключ
    # _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Преобразовываем адрес, по которому лежит фото питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Отправляем запрос на создание нового питомца с фото
    _, status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

    # Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа содержится имя питомца
    assert status == 200
    assert result['name'] == name


# test 4
@pytest.mark.positive
@pytest.mark.api
@pytest.mark.create
@pytest.mark.xfail
def test_add_new_pet_with_valid_data_png(get_key, name='Снежок', animal_type='cat', age='9',
                                         pet_photo='../images/cat.png'):
    """Тест на проверку успешного создания питомца с фото в формате png"""

    # Получаем api ключ
    # _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Преобразовываем адрес, по которому лежит фото питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Отправляем запрос на создание нового питомца с фото
    _, status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

    # Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа содержится имя питомца
    assert status == 200
    assert result['name'] == name


# test 5
@pytest.mark.positive
@pytest.mark.api
@pytest.mark.create
def test_successful_create_new_pet_without_photo(get_key, name='Кельвин', animal_type='dog', age='7'):
    """Тест на проверку успешного создания питомца без фото"""

    # Получаем api ключ
    # _, _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Отправляем запрос на создание нового питомца с фото
    _, status, result = pf.create_pet_without_photo(get_key, name, animal_type, age)

    # Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа содержится имя питомца
    assert status == 200
    assert result['name'] == name


# test 6
@pytest.mark.positive
@pytest.mark.api
@pytest.mark.delete
def test_successful_delete_pet(get_key):
    """Тест на проверку успешного удаления питомца"""

    # Получаем api ключ
    # _, _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список моих питомцев
    _, _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Если список пуст, то добавляем нового питомца
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(get_key, "Пушок", "cat", "3", "../images/cat.jpeg")
        _, _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Запоминаем id первого питомца
    pet_id = my_pets['pets'][0]['id']

    # Отправляем запрос на удаление питомца
    _, status, result = pf.delete_pet(get_key, pet_id)

    # Снова получаем список моих питомцев
    _, _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа нет id удаленного питомца
    assert status == 200
    assert pet_id not in my_pets


# test 7
@pytest.mark.positive
@pytest.mark.api
@pytest.mark.update
def test_update_pet_with_valid_date(get_key, new_name="Пончик", new_animal_type="dog", new_age="5"):
    """Тест на проверку успешного обновления питомца"""

    # Получаем api ключ
    # _, _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список моих питомцев
    _, _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Если список не пуст, то обновляем данные первого питомца
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        _, status, result = pf.update_pet(get_key, pet_id, new_name, new_animal_type, new_age)

        # Проверяем, что ответ на запрос имеет статус 200 и в тексте имя совпадает с новым именем
        assert status == 200
        assert result['name'] == new_name

    else:
        raise Exception('Нет животных для обновления')


# test 8
@pytest.mark.positive
@pytest.mark.api
@pytest.mark.update
def test_successful_add_photo(get_key, pet_photo='../images/dog.jpg'):
    """Тест на проверку успешного добавления фото питомца"""

    # Получаем api ключ
    # _, _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список моих питомцев
    _, _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Если список пуст, то добавляем нового питомца
    if len(my_pets['pets']) == 0:
        pf.create_pet_without_photo(get_key, "Эрвин", "dog", "3")
        _, _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Запоминаем id первого питомца
    pet_id = my_pets['pets'][0]['id']

    # Преобразовываем адрес, по которому лежит фото питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Отправляем запрос на добавление фото питомца
    _, status, result = pf.add_pet_photo(get_key, pet_id, pet_photo)

    # Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа есть поле с фото
    assert status == 200
    assert result['pet_photo'] != ""


# Негативные тесты

# test 9
@pytest.mark.negative
@pytest.mark.api
@pytest.mark.auth
@pytest.mark.skip(reason="Не использует фикстуру get_key")
def test_get_api_key_for_invalid_user(email="q@q.q", password="q"):
    """Тест на проверку получения api ключа c невалидными данными"""

    # Отправляем запрос на получение api ключа
    _, status, result = pf.get_api_key(email, password)

    #  Проверяем, что ответ на запрос имеет статус 403
    assert status == 403


# test 10
@pytest.mark.negative
@pytest.mark.api
@pytest.mark.auth
@pytest.mark.skip(reason="Не использует фикстуру get_key")
def test_get_api_key_for_user_with_empty_data(email="", password=""):
    """Тест на проверку получения api ключа c пустыми полями"""

    # Отправляем запрос на получение api ключа
    _, status, result = pf.get_api_key(email, password)

    #  Проверяем, что ответ на запрос имеет статус 403
    assert status == 403


# test 11
@pytest.mark.negative
@pytest.mark.api
@pytest.mark.get
@pytest.mark.skip(reason="Не использует фикстуру get_key")
def test_get_all_pets_with_empty_auth_key(filter=''):
    """Тест на проверку получения списка всех питомцев с пустым api ключом"""

    # Создаем пустой ключ
    auth_key = {'key': ''}

    # Отправляем запрос на получение списка всех питомцев
    _, status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем, что ответ на запрос имеет статус 403
    assert status == 403


# test 12
@pytest.mark.negative
@pytest.mark.api
@pytest.mark.get
@pytest.mark.skip(reason="Не использует фикстуру get_key")
def test_get_all_pets_with_invalid_auth_key(filter=''):
    """Тест на проверку получения списка всех питомцев с невалидным api ключом"""

    # Создаем невалидный ключ
    auth_key = {'key': '123'}

    # Отправляем запрос на получение списка всех питомцев
    _, status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем, что ответ на запрос имеет статус 403
    assert status == 403


# test 13
@pytest.mark.negative
@pytest.mark.api
@pytest.mark.get
def test_get_all_pets_with_invalid_filter(get_key, filter='dogs'):
    """Тест на проверку получения списка питомцев с несуществующим фильтром"""

    # Получаем api ключ
    # _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Отправляем запрос на получение списка всех питомцев
    _, status, result = pf.get_list_of_pets(get_key, filter)

    # Проверяем, что ответ на запрос имеет статус 500
    assert status == 500


# test 14
@pytest.mark.negative
@pytest.mark.api
@pytest.mark.create
def test_add_new_pet_with_invalid_photo(get_key, name='Барсик', animal_type='cat', age='2',
                                        pet_photo='../images/example.pdf'):
    """Тест на проверку создания питомца, вместо фото pdf-файл"""

    # Получаем api ключ
    # _, _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Преобразовываем адрес, по которому лежит фото питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Отправляем запрос на создание нового питомца с фото
    _, status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

    # Проверяем, что ответ на запрос имеет статус 500
    assert status == 500


# test 15
@pytest.mark.negative
@pytest.mark.api
@pytest.mark.create
@pytest.mark.skip(reason="Не использует фикстуру get_key")
def test_add_new_pet_with_invalid_auth_key(name='Шарик', animal_type='dog', age='7', pet_photo='../images/dog.jpg'):
    """Тест на проверку создания питомца c невалидным ключом"""

    # Создаем невалидный api ключ
    auth_key = {'key': 'invalid'}

    # Преобразовываем адрес, по которому лежит фото питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Отправляем запрос на создание нового питомца с фото
    _, status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем, что ответ на запрос имеет статус 403
    assert status == 403


# test 16
@pytest.mark.negative
@pytest.mark.api
@pytest.mark.create
def test_create_new_pet_without_photo_with_empty_data(get_key, name='', animal_type='', age=''):
    """Тест на проверку создания питомца без фото, с пустыми данными"""

    # Получаем api ключ
    # _, _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Отправляем запрос на создание нового питомца с фото
    _, status, result = pf.create_pet_without_photo(get_key, name, animal_type, age)

    # Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа содержится пустое имя питомца
    assert status == 200
    assert result['name'] == ''


# test 17
@pytest.mark.negative
@pytest.mark.api
@pytest.mark.create
def test_create_new_pet_without_photo_with_literal_age(get_key, name='Марта', animal_type='cow', age='бесконечность'):
    """Тест на проверку создания питомца без фото, если значение возраста состоит из букв"""

    # Получаем api ключ
    # _, _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Отправляем запрос на создание нового питомца с фото
    _, status, result = pf.create_pet_without_photo(get_key, name, animal_type, age)

    # Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа содержится пустое имя питомца
    assert status == 200
    assert result['age'] == age


# test 18
@pytest.mark.negative
@pytest.mark.api
@pytest.mark.update
def test_add_photo_with_invalid_pet_id(get_key, pet_photo='../images/dog.jpg'):
    """Тест на проверку добавления фото c невалидным id питомца"""

    # Получаем api ключ
    # _, _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Создаем невалидный id питомца
    pet_id = '-'

    # Преобразовываем адрес, по которому лежит фото питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Отправляем запрос на добавление фото питомца
    _, status, result = pf.add_pet_photo(get_key, pet_id, pet_photo)

    # Проверяем, что ответ на запрос имеет статус 500
    assert status == 500


# test 19
@pytest.mark.negative
@pytest.mark.api
@pytest.mark.delete
def test_unsuccessful_delete_pet_with_empty_pet_id(get_key):
    """Тест на проверку неуспешного удаления питомца, по пустому pet_id"""

    # Получаем api ключ
    # _, _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Создаем пустой pet_id
    pet_id = ''

    # Отправляем запрос на удаление питомца
    _, status, result = pf.delete_pet(get_key, pet_id)

    # Проверяем, что ответ на запрос имеет статус 404
    assert status == 404
