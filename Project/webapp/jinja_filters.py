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


def format_datetime(value, format='%d-%m-%Y'):
    return value.strftime(format)


def set_time_match(value):
    if value == "min":
        return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
    if value == "max":
        timenow = datetime.datetime.now()
        return timenow.replace(year=timenow.year + 1).strftime("%Y-%m-%dT00:00")
    return "Error"


def count_match(idteam):
    return utils.countmatch(idteam)


def HS(idteam):
    BT = 0
    BB = 0
    win = utils.get_win_match(idteam)
    for i in win:
        BT += i.winnergoals
        BB += i.losergoals
    lose = utils.get_lose_match(idteam)
    for i in lose:
        BT += i.losergoals
        BB += i.winnergoals
    tie = utils.get_tie_match(idteam)
    for i in tie:
        BT += i.winnergoals
        BB += i.losergoals
    return BT - BB


def Score(idteam):
    diem = 0
    config = models.Config.query.first()
    diem = len(utils.get_win_match(idteam)) * config.winScore + len(utils.get_tie_match(idteam)) * config.tieScore + len(
        utils.get_lose_match(idteam)) * config.loseScore
    return diem


app.jinja_env.filters['encodeID'] = encodeID
app.jinja_env.filters['format_datetime'] = format_datetime
app.jinja_env.filters['set_time_match'] = set_time_match
app.jinja_env.filters['count_match'] = count_match
app.jinja_env.filters['HieuSo'] = HS
app.jinja_env.filters['Score'] = Score
