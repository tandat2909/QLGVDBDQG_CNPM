import os
import datetime

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


def format_datetime(value):
    return value.strftime("%d-%m-%Y %HH:%m ")


def set_time_match(value):
    if value == "min":
        return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
    if value == "max":
        timenow = datetime.datetime.now()
        return timenow.replace(year=timenow.year+1).strftime("%Y-%m-%dT00:00")
    return "Error"

app.jinja_env.filters['encodeID'] = encodeID
app.jinja_env.filters['format_datetime'] = format_datetime
app.jinja_env.filters['set_time_match'] = set_time_match
