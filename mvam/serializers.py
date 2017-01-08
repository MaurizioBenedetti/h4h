from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

from . import models


class RespondentSerializer(ModelSerializer):

    class Meta:
        model = models.Respondent


class LanguageSerializer(ModelSerializer):

    class Meta:
        model = models.Language


class LocationTypeSerializer(ModelSerializer):

    class Meta:
        model = models.LocationType


class OccupationSerializer(ModelSerializer):

    class Meta:
        model = models.Occupation


class DeviceTypeSerializer(ModelSerializer):

    class Meta:
        model = models.DeviceType


class ResponseSerializer(ModelSerializer):

    class Meta:
        model = models.Response


class LocationsSerializer(ModelSerializer):

    class Meta:
        model = models.Locations


class SurveyTypeSerializer(ModelSerializer):

    class Meta:
        model = models.SurveyType


class SurveySerializer(ModelSerializer):

    class Meta:
        model = models.Survey
