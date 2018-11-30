from statistics import median
from typing import Optional
from datetime import datetime, date
from statistics import median

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    data = get_friends(user_id, 'bdate')
    friends = [User(**friend) for friend in data['response']['items']]
    ages = []
    for friend in friends:
        if friend.bdate is not None:
            if len(friend.bdate) >= 8:
                ages.append((datetime.today() - datetime.strptime(friend.bdate, '%d.%m.%Y')).days // 365.25)
    if len(ages) > 0:
        age = median(ages)
        return age
    else:
        return None
