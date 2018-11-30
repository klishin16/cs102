import requests
import time
import config
from api_models import Message


def get(url: str, params: dict={}, timeout: int=5, max_retries: int=5, backoff_factor: float=0.3):
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for repeat in range(max_retries):
        try:
            response = requests.get(url, params, timeout=timeout)
            return response
        except requests.exceptions.RequestException:
            if repeat >= max_retries - 1:
                raise
            else:
                time.sleep(backoff_factor * (2 ** repeat))


def get_friends(user_id, fields='bdate'):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    url = config.VK_CONFIG.get('domain')
    url += "friends.get"
    access_token = config.VK_CONFIG.get('access_token')
    version = config.VK_CONFIG.get('version')
    query_params = {
        'access_token': access_token,
        'user_id': user_id,
        'v': version,
        'fields': fields
    }
    response = get(url, params=query_params)
    return response.json()


def messages_get_history(user_id, offset=0, count=300):
    """ Получить историю переписки с указанным пользователем
    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"

    url = config.VK_CONFIG.get('domain')
    url += "messages.getHistory"
    access_token = config.VK_CONFIG.get('access_token')
    version = config.VK_CONFIG.get('version')

    messages = []
    while True:
        query_params = {
            'access_token': access_token,
            'user_id': user_id,
            'v': version,
            'offest': offset,
            'count': min(count, 200)
        }
        response = get(url, params=query_params)
        gotHistory = response.json()["response"]["items"]
        for message in gotHistory:
            messages.append(Message(**message))

        if count < 200:
            break
        else:
            time.sleep(1)
            count -= 200
    return messages
