from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user = models.CharField(max_length=255, unique=True)
    pass_w = models.CharField(max_length=50)
    email = models.EmailField('Adresse mail', unique=True)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)

    STUDENT = 1
    PROFESSOR = 2

    ROLE_CHOICES = (
        (STUDENT, 'Student'),
        (PROFESSOR, 'Professor'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
