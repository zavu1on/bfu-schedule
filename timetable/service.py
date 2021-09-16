import datetime
from copy import deepcopy

one_day = datetime.timedelta(days=1)


def get_week(date):
    day_idx = (date.weekday() + 1) % 7
    sunday = date - datetime.timedelta(days=day_idx)
    date = sunday
    for n in range(7):
        yield date
        date += one_day


def get_button(request):
    return request.body.decode('utf8').split('&')[-1].split('=')[1]


def get_month(start: datetime.datetime, end: datetime.datetime):
    date = deepcopy(start)
    for n in range(start.day, end.day + 1):
        yield date
        date += one_day


def get_pair_times():
    return [
        ('8.30', '10.00'),
        ('10.10', '11.40'),
        ('11.50', '13.20'),
        ('13.50', '15.20'),
        ('15.30', '17.00'),
        ('17.10', '18.40')
    ]
