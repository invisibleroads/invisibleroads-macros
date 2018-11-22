from datetime import datetime


DATESTAMP_FORMAT = '%Y%m%d'
TIMESTAMP_FORMAT = DATESTAMP_FORMAT + '-%H%M'


def get_timestamp(x=None, with_microsecond=False):
    if x is None:
        x = datetime.now()
    if with_microsecond:
        return x.strftime(TIMESTAMP_FORMAT + '-%f')
    else:
        return x.strftime(TIMESTAMP_FORMAT)


def parse_timestamp(text):
    for FORMAT in DATESTAMP_FORMAT, TIMESTAMP_FORMAT:
        try:
            return datetime.strptime(text, FORMAT)
        except ValueError:
            pass
    else:
        raise ValueError


format_timestamp = get_timestamp
