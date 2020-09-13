import time
import schedule

def ScheduleTimer(conf, callback, symbols, interval=1, ScheduleTime="00:00"):
    schedule.clear()

    if symbols == "seconds":
        schedule.every(interval).seconds.do(callback, conf)
    if symbols == "minutes":
        schedule.every(interval).minutes.do(callback, conf)
    if symbols == "hour":
        schedule.every(interval).hour.do(callback, conf)
    if symbols == "day":
        schedule.every(interval).day.at(ScheduleTime).do(callback, conf)

    while True:
        # 启动服务
        schedule.run_pending()
        time.sleep(1)

def FileLoggingInit(file):
    logger = logging.getLogger()
    logger.setLevel(level = logging.INFO)
    handler = logging.FileHandler(file)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger