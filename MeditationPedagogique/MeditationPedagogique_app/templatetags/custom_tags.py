from atexit import register
from django import template

from ..models import Question, Answer
from django.utils import timezone
import statistics

register = template.Library()

@register.simple_tag
def count_non_hidden_comments(comments):
    count = 0
    for comment in comments:
        if not comment.hidden:
            count+=1

    return count


@register.simple_tag
def count_hidden_comments(comments):
    count = 0
    for comment in comments:
        if comment.hidden:
            count+=1
    return count

@register.simple_tag
def getAnswerText(user, question):
    answer = question.answer_of_question.all().filter(user=user).first()
    if answer != None:
        return answer.answerText
    else:
        return ''

@register.simple_tag
def getAnswerNumber(user, question):
    answer = question.answer_of_question.all().filter(user=user).first()
    if answer != None:
        return answer.answerNumber
    else:
        return "-1"

@register.simple_tag
def hasAnswered(evaluation, user_answerer):
    questionIds = evaluation.question_of_evaluation.all().values('id')
    alreadyAnswered = False
    for questionId in questionIds:
        question = Question.objects.get(pk=questionId['id'])
        
        #Check if user already answered this question or not:
        if Answer.objects.filter(user=user_answerer, question=question).exists():
            alreadyAnswered = True
    return alreadyAnswered


@register.simple_tag
def getMinimalAnswer(question):
    answers = list(question.answer_of_question.all().values('answerNumber'))
    if len(answers)>0:
        results = [result['answerNumber'] for result in answers]
        return min(results)
    else:
        return "-1"

@register.simple_tag
def getMaximalAnswer(question):
    answers = list(question.answer_of_question.all().values('answerNumber'))
    if len(answers)>0:
        results = [result['answerNumber'] for result in answers]
        return max(results)
    else:
        return "-1"

@register.simple_tag
def getMeanAnswer(question):
    answers = list(question.answer_of_question.all().values('answerNumber'))
    if len(answers)>0:
        results = [result['answerNumber'] for result in answers]
        return sum(results)/len(results)
    else:
        return "-1"

@register.simple_tag
def getStdAnswer(question):
    answers = list(question.answer_of_question.all().values('answerNumber'))
    if len(answers)>0:
        results = [result['answerNumber'] for result in answers]
        return statistics.pstdev(results)
    else:
        return "-1"
    

@register.simple_tag
def finalEvaluation(order):
    if order>=3000:
        return True
    else:
        return False

@register.simple_tag
def finalEvaluationCreated(elements):
    for element in elements:
        if element.order>3000:
            return True
    return False