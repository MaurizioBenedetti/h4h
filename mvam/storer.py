from . import models
import datetime ## need to add this .. (if doing dates manually is necessary)


def store_response(response):
    """

    :param question_id: the id of the SurveyQuestion
    :param response: an array of response metrics
    :return: None
    """
    # store Response
    timestamp = response["timestamp"]
    respondent_id = response["respondent"]["respondent_id"]
    raw_response = response["raw_response"]
    question_id = response["question"]["question_id"]
    session_id = response["session_id"]

    survey_question = models.SurveyQuestion.objects.get(question = question_id) # query for survey where question = question_id.   do we need a try/catch??
    survey = mosels.Survey.objects.get(survey_id = survey_question.id) # survey_question.survey_question.id???
    #survey_question.survey = survey

    res = models.Response(timestamp = timestamp, respondent = respondent_id, raw_response = raw_response,
            question = question_id, survey = survey, session_id = session_id)

    res.save()
    # store the survey object

    for metric in response["metrics"]:
        metric_id = metric["metric_id"]
        value = metric["score"]
        metric_res = models.MetricResponse(timestamp = timestamp,
                response = res.id, metric = metric_id, value = value)
        metric_res.save()

    return
