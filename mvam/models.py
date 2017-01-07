from __future__ import unicode_literals

from django.db import models


class Respondent(models.Model):

    GENDERS = (
        ('M', 'male'),
        ('F', 'female'),
        ('U', 'unknown')
    )

    respondent_id = models.CharField(max_length=256, primary_key=True)
    location = models.CharField(max_length=100)
    location_type = models.ForeignKey('LocationType')
    device_type = models.ForeignKey('DeviceType', blank=True, null=True)
    gender = models.CharField(max_length=5, choices=GENDERS, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    occupation = models.ForeignKey('Occupation')
    income = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.respondent_id)

    def __str__(self):
        return str(self.respondent_id)


class LocationType(models.Model):

    model = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.model)

    def __str__(self):
        return str(self.model)


class Occupation(models.Model):

    occupation = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.occupation)

    def __str__(self):
        return str(self.occupation)


class DeviceType(models.Model):

    device_type = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.device_type)

    def __str__(self):
        return str(self.device_type)