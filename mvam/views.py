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
from rest_framework.views import APIView

from . import serializers, models, scorer, storer


class HandleResponse(APIView):

    def is_new_survey(self, request):

        try:
            _ = request.data['question']['question_id']
            return False
        except KeyError:
            return True

    def post(self, request):

        # is this a new survey
        if self.is_new_survey(request):

            # do I have a location
            try:
                location = request.data['respondent']['location']
            except KeyError:
                return Response({'STATUS': 'NO LOCATION'})
            # is demo required

            return Response({'STATUS': 'NEW SURVEY'})

        # if it isn't a new question, but we didn't get any response
        # respond with the same question
        try:
            raw_response = request.data['raw_response']
            question_id = request.data['question']['question_id']
            responses = request.data['question']['metrics']

        # if we didn't actually get a response, we just respond with the same
        # object
        except KeyError:
            return Response(request.data)

        # now we know that we actually need to process the response
        # first store the response metrics
        storer.store_response(
            question_id,
            responses
        )

        # then we need to score the response
        next_question = scorer.score_response(
            question_id,
            responses
        )

        # format a new response based on the next question

        return Response({'STATUS': 'NEXT QUESTION'})

class RespondentViewset(viewsets.ModelViewSet):
    serializer_class = RespondentSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
    queryset = models.Respondent.objects.all()


class LanguageViewset(viewsets.ModelViewSet):
    serializer_class = LanguageSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
    queryset = models.Language.objects.all()


class LocationTypeViewset(viewsets.ModelViewSet):
    serializer_class = LocationTypeSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
    queryset = models.LocationType.objects.all()


class OccupationViewset(viewsets.ModelViewSet):
    serializer_class = OccupationSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
    queryset = models.Occupation.objects.all()


class DeviceTypeViewset(viewsets.ModelViewSet):
    serializer_class = DeviceTypeSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
    queryset = models.DeviceType.objects.all()


class ResponseViewset(viewsets.ModelViewSet):
    serializer_class = ResponseSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
    queryset = models.Response.objects.all()


class LocationsViewset(viewsets.ModelViewSet):
    serializer_class = LocationsSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
    queryset = models.Locations.objects.all()


class SurveyTypeViewset(viewsets.ModelViewSet):
    serializer_class = SurveyTypeSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
    queryset = models.SurveyType.objects.all()


class SurveyViewset(viewsets.ModelViewSet):
    serializer_class = SurveySerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
    queryset = models.Survey.objects.all()

