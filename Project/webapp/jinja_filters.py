import os
from datetime import datetime

from webapp import utils
from webapp import app
import datetime
import uuid

def encodeID(value):
    try:
        en = utils.encodeID(value)
        return en
    except:
        return ''
def format_datetime(value,format = '%d-%m-%Y'):

    return value.strftime(format)


app.jinja_env.filters['encodeID'] = encodeID
app.jinja_env.filters['format_datetime'] = format_datetime
