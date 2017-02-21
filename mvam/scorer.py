from . import models
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError, ParseError


def get_question_rules(question):

    print question

    return models.SurveyQuestionRule.objects.filter(
        survey_question=question
    )


def get_question_rules_args(question_rule):

    return models.SurveyQuestionRulesArgument.objects.filter(
        survey_question_rules=question_rule
    )


def score_response(response):
    """

    :param question_id: the id of the SurveyQuestion
    :param response: an array of response metrics
    :return: the next SurveyQuestion or a TERMINATE message
    """

    TERMINATE = {
        'on_next': 'TERMINATE',
        'message': 'Thanks for your input! Check back soon!'
    }


    survey_question = response['question']['question_id']
    question = response['question']['question_id'].question


    # sift out inactive SurveyQuestionRules
    active_rules = []
    for rule in get_question_rules(survey_question):
        print rule
        if rule.is_active:
            active_rules.append(rule)

    if len(active_rules) is 0:
        return TERMINATE

    potentials = []

    for rule in active_rules:
        print rule
        args = get_question_rules_args(rule)
        print args
        for arg in args:
            for _metric in response['question']['metrics']:

                try:
                    metric = models.Metric.objects.get(id=_metric['metric_id'])
                except ObjectDoesNotExist:
                    raise ParseError('bad metric id')

                print('_metric: {}'.format(_metric))
                print('metric: {}').format(metric)

                if _metric["metric_id"] == arg.metric.id:

                    print('type: {}'.format(metric.metric_type.format))
                    print('{} - {} - {}'.format(
                        str(_metric["metric_value"]),
                        str(arg.operator.operator),
                        str(arg.value))
                    )
                    if metric.metric_type.format == 'N':
                        print 'numeric'
                        if arg.operator.operator == ">":
                            if _metric["metric_value"] > int(arg.value):
                                potentials.append(rule)

                        if arg.operator.operator == "<":
                            if _metric["metric_value"] < int(arg.value):
                                potentials.append(rule)

                        if arg.operator.operator == "=":
                            if _metric["metric_value"] == int(arg.value):
                                potentials.append(rule)

                        if arg.operator.operator == "<=":
                            if _metric["metric_value"] <= int(arg.value):
                                potentials.append(rule)

                        if arg.operator.operator == ">=":
                            if _metric["metric_value"] >= int(arg.value):
                                potentials.append(rule)
                        if arg.operator.operator == "*":
                            potentials.append(rule)

                    if metric.metric_type.format == 'S':
                        if arg.operator.operator == "~":
                            if str(_metric["metric_value"]) in str(arg.value):
                                potentials.append(rule)
                        if arg.operator.operator == "=":
                            if str(_metric["metric_value"]) == str(arg.value):
                                potentials.append(rule)
                        if arg.operator.operator == "*":
                            potentials.append(rule)

    if len(potentials) is 0:
        return TERMINATE

    # sort potentials on highest rules_priority
    try:
        top = potentials[0]
        for potential in potentials:
            if potential.rules_priority > top.rules_priority:
                top = potential
    except IndexError:
        return TERMINATE

    if top.next_question is not None:
        return top.next_question
    else:
        return TERMINATE
