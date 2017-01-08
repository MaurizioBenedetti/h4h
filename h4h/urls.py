"""h4h URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from mvam import views

router = routers.DefaultRouter()
router.register(r'respondent', views.RespondentView)
router.register(r'language', views.LanguageView)
router.register(r'location_type', views.LocationTypeView)
router.register(r'occupation', views.OccupationView)
router.register(r'device_type', views.DeviceTypeView)
router.register(r'response', views.ResponseView)
router.register(r'locations', views.LocationsView)
router.register(r'survey_type', views.SurveyTypeView)
router.register(r'survey', views.SurveyView)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
]
