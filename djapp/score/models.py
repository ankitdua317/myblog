from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Match(models.Model):
	name = models.CharField(max_length=30, unique=True)
	home = models.IntegerField(blank=False, null=False)
	away = models.IntegerField(blank=False, null=False)
	def __unicode__(self):
		return self.name
	def __str__(self):
		return self.name