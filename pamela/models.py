from django.db import models

class stat(models.Model):
	time = models.DateTimeField()
	nbComputerUp = models.IntegerField()

class userNames(models.Model):
	name = models.CharField(max_length=200)
