import datetime

import pytz



def utcnow():

    return datetime.datetime.now(pytz.timezone('Etc/GMT-5'))