import time
import schedule
import threading
import json
import logging


def ScheduleTimer(Parm, callback, symbols, interval=1, Tag=None, ScheduleTime="00:00"):
    if symbols == "seconds":
        schedule.every(interval).seconds.do(callback, Parm).tag(Tag)
    if symbols == "minutes":
        schedule.every(interval).minutes.do(callback, Parm).tag(Tag)
    if symbols == "hour":
        schedule.every(interval).hour.do(callback, Parm).tag(Tag)
    if symbols == "day":
        schedule.every(interval).day.at(ScheduleTime).do(callback, Parm).tag(Tag)

def FileLoggingInit(file):
    logger = logging.getLogger()
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler(file)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger


def JsonFileLoad(file):
    with open(file) as json_file:
        try:
            data = json.load(json_file)
        except:
            data = {}
        return data


def ThreadCreate(func, parm, name=None):
    t = threading.Thread(target=func, args=parm)
    if name:
        t.setName(name)
    t.start()
    return t


# 时间转换接口
def Time2Sec(Time,Type):
    mon, week, day, hour, min, sec = Time.strip().split(":")
    Sec = int(mon) * 30 * 24 * 60 * 60 + int(week) * 7 * 24 * 60 * 60 + int(day) * 24 * 60 * 60 + int(hour) * 60 * 60 + int(min) * 60 + int(sec)
    return Sec


class TradeStatus:
    ON = 1
    OFF = 2
    SUSPEND = 3
