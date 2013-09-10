import datetime
import pytz
import re

def parse_fuzzy_time(s):
    split = s.split(':')
    x = len(split)

    if x in (2, 3):
        hour = int(split[0])
        minute = int(split[1])
        second = int(split[2]) if x == 3 else 0
        return datetime.time(hour, minute, second)

    return None

def convert_year(s, assumed_year):
    if len(s) == 4:
        return int(s)
    elif len(s) == 2:
        assumed_century = assumed_year - (assumed_year % 100)
        return int(s) + assumed_century
    else:
        return None

def parse_fuzzy_date(s, assumed_date):
    if s is None:
        return assumed_date

    split = s.split('/')
    x = len(split)

    if x in (1, 2, 3):
        day = int(split[0])
        month = int(split[1]) if x >= 2 else assumed_date.month
        year = convert_year(split[2], assumed_date.year) if x >= 3 else assumed_date.year
        return datetime.date(year, month, day)

    return None

_re_date_txt = r'\d\d?(/\d\d?(/\d\d(\d\d)?)?)?'
_re_time_txt = r'\d\d?:\d\d?(?::\d\d?)?'
_re_datetime_txt = r' *(?:(?P<date1>{re_date}) +)?(?P<time>{re_time})(?: +(?P<date2>{re_date}))? *$'.format(re_date=_re_date_txt, re_time=_re_time_txt)
re_datetime = re.compile(_re_datetime_txt)
def parse_fuzzy_datetime(s, current_datetime):
    m = re_datetime.match(s)

    if not m or (m.group('date1') and m.group('date2')):
        return None

    time_match = m.group('time')
    date_match = m.group('date1') or m.group('date2')

    time = parse_fuzzy_time(time_match)
    if not time:
        return None

    # If input time has already passed, assume today, else assume yesterday.
    assumed_date = current_datetime.date()
    if time > current_datetime.time():
        assumed_date = assumed_date - datetime.timedelta(days=1)

    date = parse_fuzzy_date(date_match, assumed_date)

    return datetime.datetime.combine(date, time)
