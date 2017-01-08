from . import views
from rest_framework.urls import url

routes = (
    (r'devicetype', views.DeviceTypeViewSet, 'devicetype'),
    (r'respondent', views.RespondentViewset, 'respondent'),
    (r'language', views.LanguageViewset, 'language'),
    (r'locationtype', views.LocationTypeViewset, 'locationtype'),
    (r'occupation', views.OccupationViewset, 'occupation'),
    (r'response', views.ResponseViewset, 'response'),
    (r'location', views.LocationsViewset, 'location'),
    (r'surveytype', views.SurveyViewset, 'surveytype'),
    (r'survey', views.SurveyViewset, 'survey'),
    (r'surveyquestion', views.SurveyQuestionViewSet, 'surveyquestion'),
    (r'surveyquestionrule', views.SurveyQuestionRuleViewSet, 'surveyquestionrule'),
    (r'surveyquestionruleargument', views.SurveyQuestionRuleArgumentViewSet, 'surveyquestionruleargument'),
    (r'labels', views.LabelViewset, 'labels'),
    (r'metrictypes', views.MetricTypeViewset, 'metrictypes'),
    (r'metric', views.MetricViewSet, 'metric'),
    (r'question', views.QuestionViewSet, 'question'),
    (r'questionlabel', views.QuestionLabelViewset, 'questionlabel'),
    (r'questionmetric', views.QuestionMetricViewset, 'questionmetric'),
    (r'metricresponse', views.MetricResponseViewset, 'metricresponse'),
)