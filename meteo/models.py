from django.db import models
from datetime import datetime
from time import time

class Light(models.Model):
	ltstamp = models.IntegerField(primary_key=True)
	inside = models.DecimalField(max_digits=4, decimal_places=1)
	outside = models.DecimalField(max_digits=4, decimal_places=1)

	@classmethod
	def new(klass, **kwargs):
		return klass.objects.create(ltstamp=time()*1000, **kwargs)

	def time(self):
		return datetime.fromtimestamp(self.ltstamp/1000)


class Temperature(models.Model):
	ttstamp = models.IntegerField(primary_key=True)
	ambiant = models.DecimalField(max_digits=4, decimal_places=1)
	radiator = models.DecimalField(max_digits=4, decimal_places=1)

	@classmethod
	def new(klass, **kwargs):
		return klass.objects.create(ttstamp=time()*1000, **kwargs)

	def time(self):
		return datetime.fromtimestamp(self.ltstamp/1000)
