import pytz
import datetime

def format_localtime(req, utc_time):
    localtime = to_localtime(req, utc_time)
    return localtime.strftime('%c')

def to_localtime(req, utc_time):
    """Converts datetime object to a datetime in the local system timezone."""

    settings = req.registry.settings
    tz = pytz.timezone(settings['local_timezone'])
    return utc_time.astimezone(tz)
