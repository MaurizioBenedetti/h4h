from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest_framework import serializers

from . import models


class DeviceTypeSerializer(ModelSerializer):

    class Meta:
        model = models.DeviceType


class RespondentSerializer(ModelSerializer):

    class Meta:
        model = models.Respondent
        fields = '__all__'


class LanguageSerializer(ModelSerializer):

    class Meta:
        model = models.Language
        fields = '__all__'


class LocationTypeSerializer(ModelSerializer):

    class Meta:
        model = models.LocationType
        fields = '__all__'


class OccupationSerializer(ModelSerializer):

    class Meta:
        model = models.Occupation
        fields = '__all__'


class ResponseSerializer(ModelSerializer):

    class Meta:
        model = models.Response
        fields = '__all__'


class LocationsSerializer(ModelSerializer):

    class Meta:
        model = models.Locations
        fields = '__all__'



class MetricResponseSerializer(ModelSerializer):

    response = ResponseSerializer()

    class Meta:
        model = models.MetricResponse
        fields = '__all__'


class LabelSerializer(ModelSerializer):

    class Meta:
        model = models.Label
        fields = '__all__'


class MetricTypeSerializer(ModelSerializer):

    class Meta:
        model = models.MetricType
        fields = '__all__'


class MetricSerializer(ModelSerializer):

    metric_type = MetricTypeSerializer()

    class Meta:
        model = models.Metric
        fields = '__all__'


class QuestionMetricSerializer(ModelSerializer):

    metric = MetricSerializer()

    class Meta:
        model = models.QuestionMetric
        fields = '__all__'


class QuestionSerializer(ModelSerializer):

    base_language = LanguageSerializer()

    class Meta:
        model = models.Question
        fields = '__all__'


class QuestionLabelSerializer(ModelSerializer):

    label = LabelSerializer()
    question = QuestionSerializer()

    class Meta:
        model = models.QuestionLabel
        fields = '__all__'


class SurveyTypeSerializer(ModelSerializer):

    class Meta:
        model = models.SurveyType
        fields = '__all__'


class SurveySerializer(ModelSerializer):

    class Meta:
        model = models.Survey
        fields = '__all__'


class SurveyQuestionSerializer(ModelSerializer):

    class Meta:
        model = models.SurveyQuestion
        fields = '__all__'


class SurveyQuestionRuleSerializer(ModelSerializer):

    class Meta:
        model = models.SurveyQuestionRule
        fields = '__all__'


class SurveyQuestionRulesArgumentSerializer(ModelSerializer):

    class Meta:
        model = models.SurveyQuestionRulesArgument
        fields = '__all__'
