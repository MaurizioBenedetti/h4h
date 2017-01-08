from . import models


def score_response(response):
    """

    :param question_id: the id of the SurveyQuestion
    :param response: an array of response metrics
    :return: the next SurveyQuestion or a TERMINATE message
    """

    question_id = response["question"]["question_id"]
    survey_question = models.SurveyQuestion.objects.get(question=question_id)

    # QUERY to get all SurveyQuestionRules
    all_sq_rules = models.SurveyQuestionRule.objects.filter(survey_question=survey_question)

    # sift out inactive SurveyQuestionRules
    active_sq_rules = []
    for rule in all_sq_rules:
        if rule["is_active"]:
            active_sq_rules.append(rule)


    potentials = []
    for sq_rule in active_sq_rules:
        #QUERY to get all SurveyQuestionRulesArguments objects
        sqr_arguments = models.SurveyQuestionRulesArguments.objects.filter(survey_question_rules=sq_rule)
        for sqr_argument in sqr_arguments:
            # QUERY the operator
            operator = models.Operator.objects.get(args_operator=sqr_argument["args_operator"])

            for metric in response["metrics"]:
                if metric["metric_id"] == sqr_argument["args_metric"]:
                    #run operator LOGIC to determine if rule is satisfied
                    if(operator["operator"] == ">"):
                        if (metric["value"] > sqr_argument["args_value"]):
                            potentials.append(sq_rule)
                    if(operator["operator"] == "<"):
                        if (metric["value"] < sqr_argument["args_value"]):
                            potentials.append(sq_rule)
                    if(operator["operator"] == "=" || operator["operator"] == "=="):
                        if (metric["value"] == sqr_argument["args_value"]):
                            potentials.append(sq_rule)
                    if(operator["operator"] == "<="):
                        if (metric["value"] <= sqr_argument["args_value"]):
                            potentials.append(sq_rule)
                    if(operator["operator"] == ">="):
                        if (metric["value"] >= sqr_argument["args_value"]):
                            potentials.append(sq_rule)


    # sort potentials on highest rules_priority
    potentials.sort(key=lambda potential: potential["rules_priority"])
    highest_priority = potentials.pop()

    if highest_priority["next_question"]:
        return highest_priority["next_question"]
    else:
        return "TERMINATE"









            # #QUERY to get MetricResponse value
            # metric_response = models.MetricResponse.objects.get(metric_id=sqr_argument["args_metric"])
