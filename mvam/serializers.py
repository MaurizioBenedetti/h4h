from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest_framework import serializers

from . import models


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


class DeviceTypeSerializer(ModelSerializer):

    class Meta:
        model = models.DeviceType


class ResponseSerializer(ModelSerializer):

    class Meta:
        model = models.Response
        fields = '__all__'


class LocationsSerializer(ModelSerializer):

    class Meta:
        model = models.Locations
        fields = '__all__'


class SurveyTypeSerializer(ModelSerializer):

    class Meta:
        model = models.SurveyType
        fields = '__all__'


class SurveySerializer(ModelSerializer):

    class Meta:
        model = models.Survey
        fields = '__all__'


class MetricResponseSerializer(ModelSerializer):

    class Meta:
        model = models.MetricResponse
        fields = '__all__'

class MessageRespondentField(serializers.DictField):
    respondent_id = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    location_type = serializers.CharField(max_length=255)
    language = serializers.CharField(max_length=255)
    device_type = serializers.CharField(max_length=255)


class MessageMetricsField(serializers.ListField):
    child = MetricResponseSerializer()


class MessageQuestionField(serializers.DictField):
    question_id = serializers.IntegerField()
    question_text = serializers.CharField(max_length=255)
    metrics = MessageMetricsField()


class MessageSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    session_id = serializers.CharField(max_length=255)
    respondent = MessageRespondentField()
    raw_response = serializers.CharField(max_length=255)
    question = MessageQuestionField()