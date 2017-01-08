from . import models
import datetime ## need to add this .. (if doing dates manually is necessary)


def store_response(response):
    """

    :param question_id: the id of the SurveyQuestion
    :param response: an array of response metrics
    :return: None
    """

    print response


    # store Response
    timestamp = response["timestamp"]
    respondent = response["respondent"]
    raw_response = response["raw_response"]
    question = response["question"]["question_id"]
    session_id = response["session_id"]

    survey = models.Survey.objects.get(survey__id= question.id) # survey_question.survey_question.id???

    res = models.Response(
        timestamp = timestamp,
        respondent = respondent,
        raw_response = raw_response,
        question = question,
        survey = survey,
        session_id = session_id
    )

    res.save()


    for metric in response["metrics"]:
        # query for MetricType using metric_id
        metric_type = metric["metric_type"]
        if metric_type["format"] == "S":
            types = response["raw_response"].split(',')
            for m_text_value in types:
                # store text_values and everything else into MetricResponse
                metric_res = models.MetricResponse(timestamp=timestamp,response=res.id,
                        metric=metric['metric_id'], text_value=m_text_value , confidence=response['confidence'] )  # where is confidence??
                metric_res.save()
        else:
            numeric_value = metric_type["type"]

            metric_res = models.MetricResponse(timestamp=timestamp,response=res.id,
                    metric=metric['metric_id'], numeric_value=response["raw_response"] , confidence= response['confidence'])#where is confidence??
            metric_res.save()

    return
