from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CustomUserForm
from django.contrib.auth import login
from django.contrib import messages
from .lesson import add_title
import os
import logging


# Create your views here.
def index(request):
    # Get all lectures in the DB
    context = {
        'test': 'CECI EST UN TEST'
    }
    return render(request, 'index.html', context)


def register_request(request):
    context = {}
    form = CustomUserForm(request.POST or None)
    context['form'] = form
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect(index)
        messages.error(
            request, 'Unsuccessful registration. Invalid information.')
    form = CustomUserForm()
    return render(request, 'registration/inscription.html', context)


def lesson(request, number):
    context = {}
    filename = 'lessons/lesson_' + str(number) + '.html'
    return render(request, filename, context)


def create_lesson(request):
    root = 'medias'
    next_lesson_number = len(os.listdir(root))
    medias_directory_name = os.path.join(
        root, 'lesson_' + str(next_lesson_number))
    os.makedirs(medias_directory_name, exist_ok=True)
    html_file_name = 'MeditationPedagogique_app/templates/lessons/lesson_' + \
        str(next_lesson_number) + '.html'
    with open(html_file_name, 'w') as f:
        f.writelines(["{% extends 'lessons/lesson.html' %} \n",
                      "{% block lesson_content %}  \n"
                     "{% include 'lessons/title.html' with title='Lesson " +
                      str(next_lesson_number) + " title' %} \n"
                      "{% endblock %}"])
        f.close
    return lesson(request, next_lesson_number)
