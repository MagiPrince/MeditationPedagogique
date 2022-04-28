from atexit import register
from django import template

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