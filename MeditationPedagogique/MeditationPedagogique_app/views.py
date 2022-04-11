from django.shortcuts import render, redirect
from .forms import CustomUserForm
from django.contrib.auth import login
from django.contrib import messages
import os
from .models import Lesson


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
    context['elements'] = Lesson.objects.all().filter(id=number)
    context['title'] = Lesson.objects.all().filter(id=number)[0].title
    context['lessonNumber'] = number
    return render(request, 'lessons/lesson.html', context)


def create_lesson(request):
    root = 'medias'
    next_lesson_number = len(os.listdir(root))
    medias_directory_name = os.path.join(
        root, 'lesson_' + str(next_lesson_number))
    os.makedirs(medias_directory_name, exist_ok=True)
    lessonDB = Lesson(title='Lesson title')
    lessonDB.save()

    return lesson(request, next_lesson_number)
