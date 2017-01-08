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
    survey = models.Survey.objects.get(survey_id = survey_question.id) # survey_question.survey_question.id???
    #survey_question.survey = survey

    res = models.Response(timestamp = timestamp, respondent = respondent_id, raw_response = raw_response,
            question = question_id, survey = survey, session_id = session_id)

    res.save()
    # store the survey object

    for metric in response["metrics"]:
        # query for MetricType using metric_id
        metric_type = metric["metric_type"]
        if metric_type["format"] == "S":
            types = response["raw_response"].split(',')
            for m_text_value in types:
                # store text_values and everything else into MetricResponse
                metric_res = models.MetricResponse(timestamp=timestamp,response=res.id,
                        metric=metric_id, text_value=m_text_value , confidence=response[] )  # where is confidence??
                metric_res.save()
        else:
            numeric_value = metric_type["type"]

            metric_res = models.MetricResponse(timestamp=timestamp,response=res.id,
                    metric=metric_id, numeric_value=response["raw_response"] , confidence= response[])#where is confidence??
            metric_res.save()

    return
