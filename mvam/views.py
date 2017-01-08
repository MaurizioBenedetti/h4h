from django.shortcuts import render
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.conf import settings

from rest_framework import permissions, viewsets, exceptions, status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_bulk import BulkModelViewSet
from rest_framework.exceptions import ValidationError, ParseError
from django.http import Http404
from rest_framework import status
from mvam.serializers import *

from . import serializers, models


class RespondentView(viewsets.ModelViewSet):
    serializer_class = RespondentSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
    queryset = models.Respondent.objects.all()


class LanguageView(viewsets.ModelViewSet):
    serializer_class = LanguageSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
    queryset = models.Language.objects.all()


class LocationTypeView(viewsets.ModelViewSet):
    serializer_class = LocationTypeSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
    queryset = models.LocationType.objects.all()


class OccupationView(viewsets.ModelViewSet):
    serializer_class = OccupationSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
    queryset = models.Occupation.objects.all()


class DeviceTypeView(viewsets.ModelViewSet):
    serializer_class = DeviceTypeSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
    queryset = models.DeviceType.objects.all()


class ResponseView(viewsets.ModelViewSet):
    serializer_class = ResponseSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
    queryset = models.Response.objects.all()


class LocationsView(viewsets.ModelViewSet):
    serializer_class = LocationsSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
    queryset = models.Locations.objects.all()


class SurveyTypeView(viewsets.ModelViewSet):
    serializer_class = SurveyTypeSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
    queryset = models.SurveyType.objects.all()


class SurveyView(viewsets.ModelViewSet):
    serializer_class = SurveySerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
    queryset = models.Survey.objects.all()

