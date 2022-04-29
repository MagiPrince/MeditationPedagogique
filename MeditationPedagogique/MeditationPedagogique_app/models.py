from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os
import shutil
import unicodedata
import re

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', str(input_str))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

class User(AbstractUser):
    user = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    email = models.EmailField('Adresse mail', unique=True)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)

    STUDENT = 1
    PROFESSOR = 2

    ROLE_CHOICES = (
        (STUDENT, 'Student'),
        (PROFESSOR, 'Professor'),
    )
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, blank=True, null=True)


class Ressource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    path = models.CharField(max_length=255, blank=False)
    lesson = models.PositiveSmallIntegerField(blank=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=False)

    slug = models.CharField(max_length=255, blank=True, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = "{}".format(re.sub(r"[^\w\s]", '_', remove_accents((self.path).lower().split('/')[-1])).replace(' ', '_'))
            print(self.slug)
            path = os.path.join(settings.MEDIA_ROOT, self.slug)
            if not os.path.isdir(path):
                os.mkdir(path)
        super(Ressource, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.path))
        super().delete(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE, related_name='comment_of_ressource')
    date = models.DateTimeField(blank=False)
    text = models.TextField(blank=True, null=True)
    hidden = models.BooleanField(blank=True, default=False)


class Type(models.Model):
    name = models.CharField(max_length=255, blank=False)


class Lesson(models.Model):
    title = models.CharField(max_length=255, blank=False)
    slug = models.CharField(max_length=255, blank=True, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = "{}".format(re.sub(r"[^\w\s]", '_', remove_accents((self.title).lower())).replace(' ', '_'))
            path = os.path.join(settings.MEDIA_ROOT, self.slug)
            if not os.path.isdir(path):
                os.mkdir(path)
        super(Lesson, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        lesson_directory = os.path.join(settings.MEDIA_ROOT, self.slug)
        #lesson_directory = os.path.join(root, 'lesson_' + str(lesson_id))
        shutil.rmtree(lesson_directory)
        super(Lesson, self).delete(*args, **kwargs)


class Element(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(blank=False)
    path = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

class GeneralInformation(models.Model):
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False, null=True)

class InscriptionCode(models.Model):

    STUDENT = 1
    PROFESSOR = 2

    ROLE_CHOICES = (
        (STUDENT, 'Student'),
        (PROFESSOR, 'Professor'),
    )
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, blank=True, null=True)

    code = models.CharField(max_length=50, blank=False, null=False)


class Question(models.Model):
    evaluation = models.ForeignKey(Element, on_delete=models.CASCADE, related_name='question_of_evaluation')
    text = models.CharField(max_length=255, blank=False)
    
    TEXT = 1
    NUMBER = 2

    TYPE_CHOICES = (
        (TEXT, 'text'),
        (NUMBER, 'number'),
    )
    type = models.PositiveSmallIntegerField(
        choices=TYPE_CHOICES, blank=True, null=True)


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_of_question')
    date = models.DateTimeField(blank=False)
    answerNumber = models.PositiveSmallIntegerField(blank=True, null=True)
    answerText = models.TextField(blank=True, null=True)
