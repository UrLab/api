from django.db import models

class Stat(models.Model):
	time = models.DateTimeField()
	nbComputerUp = models.IntegerField()

	def __unicode__(self):
		return '({}, {})'.format(self.time, self.nbComputerUp)

class UserNames(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name
