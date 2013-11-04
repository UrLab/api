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

def ISOtime2JStstamp(timestr):
	for fmt in FORMATS:
		try:
			time = datetime.strptime(timestr, fmt)
			return 1000*mktime(time.timetuple())
		except:
			pass
	raise ValueError
