from time import mktime
from datetime import datetime

FORMATS = (
	'%Y-%m-%d %H:%M:%S.%f',
	'%Y-%m-%d %H:%M:%S',
	'%Y-%m-%d %H:%M',
	'%Y-%m-%d %H',
	'%Y-%m-%d',
	'%Y-%m'
)

def datetime2JStstamp(time):
	return 1000*mktime(time.timetuple())


def ISOtime2JStstamp(timestr):
	for fmt in FORMATS:
		try:
			time = datetime.strptime(timestr, fmt)
			return datetime2JStstamp(time)
		except:
			pass
	raise ValueError