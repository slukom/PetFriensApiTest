from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Тест на проверку получения api ключа"""

    # Отправляем запрос на получение api ключа
    status, result = pf.get_api_key(email, password)

    #  Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа содержится поле 'key'
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter = ''):
    """Тест на проверку получения списка всех питомцев"""

    # Получаем api ключ
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Отправляем запрос на получение списка всех питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа содержится список питомцев
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барсик', animal_type='cat', age='2', pet_photo='../images/cat.jpeg'):
    """Тест на проверку успешного создания питомца с фото"""

    # Получаем api ключ
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Преобразовываем адрес, по которому лежит фото питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Отправляем запрос на создание нового питомца с фото
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа содержится имя питомца
    assert status == 200
    assert result['name'] == name


def test_successful_create_new_pet_without_photo(name='Кельвин', animal_type='dog', age='7'):
    """Тест на проверку успешного создания питомца без фото"""

    # Получаем api ключ
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Отправляем запрос на создание нового питомца с фото
    status, result = pf.create_pet_without_photo(auth_key, name, animal_type, age)

    # Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа содержится имя питомца
    assert status == 200
    assert result['name'] == name


def test_successful_delete_pet():
    """Тест на проверку успешного удаления питомца"""

    # Получаем api ключ
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список моих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список пуст, то добавляем нового питомца
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Пушок", "cat", "3", "../images/cat.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Запоминаем id первого питомца
    pet_id = my_pets['pets'][0]['id']

    # Отправляем запрос на удаление питомца
    status, result = pf.delete_pet(auth_key, pet_id)

    # Снова получаем список моих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа нет id удаленного питомца
    assert status == 200
    assert pet_id not in my_pets


def test_update_pet_with_valid_date(new_name = "Пончик", new_animal_type="dog", new_age="5"):
    """Тест на проверку успешного обновления питомца"""

    # Получаем api ключ
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список моих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пуст, то обновляем данные первого питомца
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.update_pet(auth_key, pet_id, new_name, new_animal_type, new_age)

        # Проверяем, что ответ на запрос имеет статус 200 и в тексте имя совпадает с новым именем
        assert status == 200
        assert result['name'] == new_name

    else:
        raise Exception('Нет животных для обновления')


def test_successful_add_photo(pet_photo='../images/dog.jpg'):
    """Тест на проверку успешного добавления фото питомца"""

    # Получаем api ключ
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список моих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список пуст, то добавляем нового питомца
    if len(my_pets['pets']) == 0:
        pf.create_pet_without_photo(auth_key, "Эрвин", "dog", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Запоминаем id первого питомца
    pet_id = my_pets['pets'][0]['id']

    # Преобразовываем адрес, по которому лежит фото питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Отправляем запрос на добавление фото питомца
    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    # Проверяем, что ответ на запрос имеет статус 200 и в тексте ответа есть поле с фото
    assert status == 200
    assert result['pet_photo'] != ""