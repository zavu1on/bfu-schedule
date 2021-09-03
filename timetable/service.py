import datetime

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
