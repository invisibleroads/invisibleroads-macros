import datetime
from dateutil.parser import parse as parse_date


def get_timestamp(with_microsecond=False):
    now = datetime.datetime.now()
    if with_microsecond:
        return now.strftime('%Y%m%d-%H%M-%f')
    else:
        return now.strftime('%Y%m%d-%H%M')


def parse_date_safely(x):
    x = str(x)
    try:
        return parse_date(x)
    except ValueError:
        # http://stackoverflow.com/questions/14595401
        return parse_date(x + '-01-01')
