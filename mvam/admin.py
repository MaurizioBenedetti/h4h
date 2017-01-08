from django.contrib import admin
from . import models

admin.site.register(models.Respondent, admin.ModelAdmin)
admin.site.register(models.DeviceType, admin.ModelAdmin)
admin.site.register(models.LocationType, admin.ModelAdmin)
admin.site.register(models.Survey, admin.ModelAdmin)
admin.site.register(models.Response, admin.ModelAdmin)
admin.site.register(models.Language, admin.ModelAdmin)
admin.site.register(models.Metric, admin.ModelAdmin)
admin.site.register(models.MetricResponse, admin.ModelAdmin)
admin.site.register(models.Label, admin.ModelAdmin)
admin.site.register(models.Question, admin.ModelAdmin)
admin.site.register(models.QuestionType, admin.ModelAdmin)
admin.site.register(models.SurveyLabel, admin.ModelAdmin)
admin.site.register(models.Occupation, admin.ModelAdmin)
admin.site.register(models.QuestionMetric, admin.ModelAdmin)
admin.site.register(models.SurveyQuestion, admin.ModelAdmin)
admin.site.register(models.SurveyQuestionRule, admin.ModelAdmin)
admin.site.register(models.SurveyQuestionRulesArgument, admin.ModelAdmin)
admin.site.register(models.Operator, admin.ModelAdmin)
admin.site.register(models.SurveyType, admin.ModelAdmin)

