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