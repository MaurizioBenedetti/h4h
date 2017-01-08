from . import views
from rest_framework.urls import url

routes = (
    (r'respondent', views.RespondentViewset, 'respondent'),
    (r'language', views.LanguageViewset, 'language'),
    (r'locationtype', views.LocationTypeViewset, 'locationtype'),
    (r'occupation', views.OccupationViewset, 'occupation'),
    (r'devicetype', views.DeviceTypeViewset, 'devicetype'),
    (r'response', views.ResponseViewset, 'response'),
    (r'location', views.LocationsViewset, 'location'),
    (r'surveytype', views.SurveyViewset, 'surveytype'),
    (r'survey', views.SurveyViewset, 'survey'),
    (r'labels', views.LabelViewset, 'labels'),
    (r'metrictypes', views.MetricTypeViewset, 'metrictypes'),
    (r'metric', views.MetricViewSet, 'metric'),
    (r'questionlabel', views.QuestionLabelViewset, 'questionlabel'),
    (r'questionmetric', views.QuestionMetricViewset, 'questionmetric'),
    (r'metricresponse', views.MetricResponseViewset, 'metricresponse'),
)