import os
from webapp import utils, models
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


def set_time_match(value):
    if value == "min":
        return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
    if value == "max":
        timenow = datetime.datetime.now()
        return timenow.replace(year=timenow.year+1).strftime("%Y-%m-%dT00:00")
    return "Error"

def amount_player(teamid):

    amount = utils.amountPlayer(teamid=teamid)

    return amount

app.jinja_env.filters['encodeID'] = encodeID
app.jinja_env.filters['format_datetime'] = format_datetime
app.jinja_env.filters['set_time_match'] = set_time_match
app.jinja_env.filters['amount_player'] = amount_player