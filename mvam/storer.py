from . import models
import datetime ## need to add this .. (if doing dates manually is necessary)
from rest_framework.exceptions import ValidationError, ParseError

def store_response(response):
    """

    :param question_id: the id of the SurveyQuestion
    :param response: an array of response metrics
    :return: None
    """


    # store Response
    timestamp = response["timestamp"]
    respondent = response["respondent"]
    raw_response = response["raw_response"]
    question = response["question"]["question_id"]
    session_id = response["session_id"]

    res = models.Response(
        timestamp=timestamp,
        respondent=respondent,
        raw_response=raw_response,
        question=question.question,
        survey=question.survey,
        session_id=session_id
    )

    res.save()

    for _metric in response['question']['metrics']:
        # query for MetricType using metric_id

        try:
            _ = _metric['metric_value']
            _ = _metric['metric_id']
        except KeyError:
            raise ParseError('metrics provided in incorrect format')

        metric = models.Metric.objects.get(
            id=_metric['metric_id']
        )
        if metric.metric_type.format == "S":
            if _metric['metric_value'] is None:
                continue
            types = _metric['metric_value'].split(',')
            for m_text_value in types:

                # store text_values and everything else into MetricResponse
                metric_res = models.MetricResponse(
                    response=res,
                    metric=metric,
                    text_value=m_text_value
                )  # where is confidence??
                metric_res.save()
        else:

            metric_res = models.MetricResponse(
                response=res,
                metric=metric,
                numeric_value=float(_metric['metric_value'])
            )
            metric_res.save()

    return
