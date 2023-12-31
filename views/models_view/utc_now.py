import datetime

import pytz



def utcnow():
    """

    Функция для установки местного времени UTC+5 вместо UTC+0,
    при создании сущности User, Article, Category

    """
    return datetime.datetime.now(pytz.timezone('Etc/GMT-5'))