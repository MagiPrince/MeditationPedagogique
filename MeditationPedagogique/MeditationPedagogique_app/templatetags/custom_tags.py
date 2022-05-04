from atexit import register
from django import template

from ..models import Question, Answer
from django.utils import timezone

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
def hasAnswered(evaluation, user_answerer):
    questionIds = evaluation.question_of_evaluation.all().values('id')
    alreadyAnswered = False
    for questionId in questionIds:
        question = Question.objects.get(pk=questionId['id'])
        
        #Check if user already answered this question or not:
        if Answer.objects.filter(user=user_answerer, question=question).exists():
            alreadyAnswered = True
    return alreadyAnswered