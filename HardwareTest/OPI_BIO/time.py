import datetime

def get_date():
    now = datetime.datetime.now()
    return now.year, now.month, now.day

def get_time():
    now = datetime.datetime.now()
    return now.hour, now.minute, now.second