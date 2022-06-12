from api import PetFriends
from settings import valid_email, valid_password, not_valid_email, not_valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    #Получаем ключ
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_wish_valid_key(filter=''):
    #Получаем список домашних питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
def test_add_new_pet_and_photo(name ='Вася', animal_type = 'кот', age= ' 4', pet_photo= 'images/cat1.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # Запрашиваем ключ api и сохраняем в переменную auth_key
    status, result = pf.add_new_pet_and_photo(auth_key, name, animal_type, age, pet_photo)  # Добавляем питомца с фото
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_not_photo(name ='Даша', animal_type = 'кошка', age= ' 1'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # Запрашиваем ключ api и сохраняем в переменную auth_key
    status, result = pf.add_new_pet(auth_key, name, animal_type, age)  # Добавляем питомца без фото
    assert status == 200
    assert result['name'] == name

def test_add_new_photo(pet_photo= 'images\cat1.jpg'): #Тест на добавление фото
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.add_new_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_successful_delete_self_pet():
     #Тест на удаление питомца
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Муся", "кошка", "1", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Кот', age=5):
    #Туст на обновление данных о питомце
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#Негативные тесты
def test_get_api_key_for_not_email(email="", password=valid_password):
    """ Тест на пустой емайл"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result

def test_get_api_key_for_not_valid_user(email=not_valid_email, password=not_valid_password):
    '''тест на неправильный емайл и пароль'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'Пользователь не найден' in result

def test_get_api_key_for_valid_user_invalid_password(email=valid_email, password=12234):
    '''Тест на неправильный пароль'''
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_for_not_email_not_password(email="", password=""):
    """ Тест на пустые поля"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result

def test_successful_update_self_not_pet_info(name='Дуня', animal_type='слон', age=5):
    '''Туст на обновление данных несуществующего питомца'''
    ''' Получаем ключ auth_key и список своих питомцев'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    ''' Если список не пустой, то пробуем обновить его имя, тип и возраст'''
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][5]['id'], name, animal_type, age)

        assert status == 403
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_successful_delete_self_not_pet():
    ''' Тест на удаление несуществующего питомца'''
    ''' Получаем ключ auth_key и запрашиваем список своих питомцев'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    '''Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев'''
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Муся", "кошка", "1")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    '''Берём id несуществующего питомца из списка и отправляем запрос на удаление'''
    pet_id = my_pets['pets'][5]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 403

def test_add_new_pet_not_photo_invalid_age(name ='Даша', animal_type = 'кошка', age= -123456989):
    '''Тест на добавление питомца с отрицательными цифрами возроста'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # Запрашиваем ключ api и сохраняем в переменную auth_key
    status, result = pf.add_new_pet(auth_key, name, animal_type, age)
    assert status == 400

def test_add_new_pet_with_invalid_photo(name="Ооо", animal_type="ДДд", age=2, pet_photo="images/riskaaa.jpg"):
    '''Тест на добавление питомца с несуществующим фото'''

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400

def test_add_new_pet_without_name(name="", animal_type="кот", age=2):
    """тест на добавление питомца с пустым полем 'name' приводит к статусу кода 400"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age)

    assert status == 400

def test_add_new_pet_not_animal_type(name="Вайс", animal_type="", age=2):
    """Тест на добавление питомца с пустым полем тип животного"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age)

    assert status == 400

