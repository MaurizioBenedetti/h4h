from __future__ import unicode_literals

from django.db import models


class Respondent(models.Model):

    GENDERS = (
        ('M', 'male'),
        ('F', 'female'),
        ('U', 'unknown')
    )

    respondent_id = models.CharField(max_length=255, primary_key=True)
    location = models.ForeignKey('Locations')
    location_type = models.ForeignKey('LocationType')
    respondent_language = models.ForeignKey('Language', blank=True, null=True)
    device_type = models.ForeignKey('DeviceType', blank=True, null=True)
    gender = models.CharField(
        max_length=5, choices=GENDERS, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    occupation = models.ForeignKey('Occupation', blank=True, null=True)
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
    raw_response = models.CharField(max_length=255)
    question = models.ForeignKey('Question')
    survey = models.ForeignKey('Survey')
    language = models.ForeignKey('Language')
    session_id = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class Locations(models.Model):
    location = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class SurveyType(models.Model):
    survey_type = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class Survey(models.Model):
    geo_scope = models.ForeignKey('Locations')
    survey_round = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(blank=True, null=True, max_length=255)
    survey_type = models.ForeignKey('SurveyType', blank=True, null=True) #foreign key to survey types
    is_demo_required = models.BooleanField()

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class SurveyQuestion(models.Model):
    survey = models.ForeignKey('Survey')
    question = models.ForeignKey('Question')

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class Metric(models.Model):

    metric_name = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class QuestionMetric(models.Model):
    metric = models.ForeignKey('Metric')
    question = models.ForeignKey('Question')

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

    question_id = models.CharField(max_length=255, primary_key=True)
    question_text = models.CharField(max_length=255)
    question_label = models.ForeignKey('Label')
    base_language = models.CharField(max_length=100)
    question_type = models.ForeignKey('QuestionType')

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


class SurveyQuestionRule(models.Model):

    survey_question = models.ForeignKey('SurveyQuestion')
    next_question = models.ForeignKey('Question')
    rules_priority = models.CharField(max_length=2)
    is_active = models.BooleanField()

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class Operator(models.Model):
    operator = models.CharField(max_length=1)

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class SurveyQuestionRulesArgument(models.Model):

    survey_question_rules = models.ForeignKey('SurveyQuestionRule')
    args_metric = models.ForeignKey('Metric')
    args_operator = models.ForeignKey('operator') #operator table
    args_value = models.IntegerField()

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)
