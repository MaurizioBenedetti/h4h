from __future__ import unicode_literals

from django.db import models


class DeviceType(models.Model):

    device_type = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.device_type)

    def __str__(self):
        return str(self.device_type)


class Label(models.Model):

    label = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.label)

    def __str__(self):
        return str(self.label)


class Language(models.Model):

    language = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.language)

    def __str__(self):
        return str(self.language)


class Locations(models.Model):
    location = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.location)

    def __str__(self):
        return str(self.location)


class LocationType(models.Model):

    location_type = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.location_type)

    def __str__(self):
        return str(self.location_type)


class Metric(models.Model):

    metric_name = models.CharField(max_length=100)
    metric_type = models.ForeignKey('MetricType')

    def __unicode__(self):
        return unicode(self.metric_name)

    def __str__(self):
        return str(self.metric_name)


class MetricType(models.Model):

    FORMATS = (
        ('N', 'NUMERIC'),
        ('S', 'STRING')
    )

    type = models.CharField(max_length=20)
    format = models.CharField(max_length=20, choices=FORMATS)

    def __unicode__(self):
        return unicode(self.type)

    def __str__(self):
        return str(self.type)


class MetricResponse(models.Model):

    timestamp = models.DateTimeField(auto_now_add=True)
    response = models.ForeignKey('Response')
    metric = models.ForeignKey('Metric')
    numeric_value = models.DecimalField(decimal_places=3, max_digits=10, blank=True, null=True)
    text_value = models.CharField(max_length=50, blank=True, null=True)
    confidence = models.DecimalField(decimal_places=3, max_digits=10, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class Occupation(models.Model):

    occupation = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.occupation)

    def __str__(self):
        return str(self.occupation)


class Operator(models.Model):
    operator = models.CharField(max_length=1)

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class Question(models.Model):

    title = models.CharField(max_length=50)
    text = models.CharField(max_length=255)
    base_language = models.ForeignKey('Language')

    def __unicode__(self):
        return unicode(self.title)

    def __str__(self):
        return str(self.title)


class QuestionLabel(models.Model):

    label = models.ForeignKey('Label')
    question = models.ForeignKey('Question')

    def __unicode__(self):
        return unicode('{} - {}'.format(self.question, self.label))

    def __str__(self):
        return str('{} - {}'.format(self.question, self.label))


class QuestionMetric(models.Model):
    metric = models.ForeignKey('Metric')
    question = models.ForeignKey('Question')

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class Respondent(models.Model):

    GENDERS = (
        ('M', 'male'),
        ('F', 'female'),
        ('U', 'unknown')
    )

    respondent_id = models.CharField(max_length=255, primary_key=True)
    location = models.ForeignKey('Locations')
    location_type = models.ForeignKey('LocationType')
    language = models.ForeignKey('Language', blank=True, null=True)
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


class Response(models.Model):

    timestamp = models.DateTimeField(auto_now_add=True)
    respondent = models.ForeignKey('Respondent')
    raw_response = models.CharField(max_length=255)
    question = models.ForeignKey('Question')
    survey = models.ForeignKey('Survey')
    language = models.ForeignKey('Language', blank=True, null=True)
    session_id = models.CharField(max_length=255)

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
    priority = models.IntegerField(default=0)
    first_question = models.ForeignKey('Question', blank=True, null=True)

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


class SurveyQuestionRule(models.Model):

    survey_question = models.ForeignKey('SurveyQuestion', related_name='survey_question')
    next_question = models.ForeignKey('SurveyQuestion', blank=True, null=True, related_name='next_question')
    rules_priority = models.CharField(max_length=2)
    is_active = models.BooleanField()

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class SurveyQuestionRulesArgument(models.Model):

    survey_question_rules = models.ForeignKey('SurveyQuestionRule')
    metric = models.ForeignKey('Metric')
    operator = models.ForeignKey('operator') #operator table
    value = models.IntegerField()

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