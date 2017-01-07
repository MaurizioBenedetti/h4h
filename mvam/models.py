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
    respondent_language = models.ForeignKey('Language')
    device_type = models.ForeignKey('DeviceType', blank=True, null=True)
    gender = models.CharField(max_length=5, choices=GENDERS, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    occupation = models.ForeignKey('Occupation')
    income = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.respondent_id)

    def __str__(self):
        return str(self.respondent_id)


class Language(models.Model):

    language = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.language)

    def __str__(self):
        return str(self.language)


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


class Response(models.Model):

    timestamp = models.DateTimeField(auto_now_add=True)
    respondent = models.ForeignKey('Respondent')
    raw_response = models.CharField(max_length=500)
<<<<<<< Updated upstream
    response_language = models.ForeignKey('Language')
    question = models.ForeignKey('Question')
    survey = models.ForeignKey('Survey')
=======
    language = models.ForeignKey('Language')
    question = models.ForeignKey('Question', blank=True, null=True)
    survey = models.ForeignKey('Survey', blank=True, null=True)
>>>>>>> Stashed changes
    session_id = models.CharField(max_length=256)

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class Survey(models.Model):

    geo_scope = models.CharField(max_length = 100)
    survey_round = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length = 100)
    description = models.CharField(blank=True, null=True, max_length=300)
    survey_type = models.CharField(max_length=256)
    questions = models.ForeignKey('Question')

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class Metric(models.Model):

    metric_name = models.CharField(max_length=100)
    metric_type = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)



class MetricResponse(models.Model):

    timestamp = models.DateTimeField()
    response = models.ForeignKey('Response')
    metric = models.ForeignKey('Metric')
    value = models.DecimalField(decimal_places=2, max_digits=4)

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class Label(models.Model):

    label = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class Question(models.Model):

    question_id = models.CharField(max_length=256, primary_key=True)
    question_text = models.CharField(max_length=500)
    question_label = models.ForeignKey('Label')
    base_language = models.CharField(max_length=100)
    question_type = models.ForeignKey('QuestionType')
    metric = models.ForeignKey('Metric')

    def __unicode__(self):
        return unicode(self.question_id)

    def __str__(self):
        return str(self.question_id)


class QuestionType(models.Model):

    question_type = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class SurveyLabel(models.Model):

    label_key = models.ForeignKey('Label')
    survey_key = models.ForeignKey('Survey')

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)