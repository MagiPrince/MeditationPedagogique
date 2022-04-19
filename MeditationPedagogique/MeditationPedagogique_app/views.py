from django.shortcuts import render, redirect
from .forms import CustomUserForm
from django.contrib.auth import login
from django.contrib import messages
import os
import shutil
from .models import Lesson, Element, Type


# Create your views here.
def index(request):
    # Get all lectures in the DB
    context = {
        'test': 'CECI EST UN TEST'
    }

    context['lessonList'] = Lesson.objects.all()

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
    lessonNumber = Lesson.objects.get(id=number)
    elements =  Element.objects.filter(lesson=lessonNumber)
    context['elements'] = elements
    context['title'] = Lesson.objects.all().filter(id=number)[0].title
    context['lessonNumber'] = number
    return render(request, 'lessons/lesson.html', context)

def add_paragraph_request(request, number, order):
    if request.method == 'POST':
        print(number)
        """ type = models.ForeignKey(Type, on_delete=models.CASCADE)
        lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
        order = models.PositiveSmallIntegerField(blank=False)
        path = models.CharField(max_length=255, blank=True, null=True)
        text = models.TextField(blank=True, null=True) """
        type = Type.objects.get(name='paragraph')
        lessonNumber = Lesson.objects.get(id=number)
        elementDB = Element(type=type, lesson=lessonNumber, order=order, text='Ceci est un paragraphe')
        elementDB.save()
    return lesson(request, number)


def create_lesson(request):
    lessonDB = Lesson(title='Lesson title')
    lessonDB.save()
    root = 'medias'
    medias_directory_name = os.path.join(
    root, 'lesson_' + str(lessonDB.id))
    os.makedirs(medias_directory_name, exist_ok=True)

    return lesson(request, lessonDB.id)


def delete_lesson(request, lesson_id):
    root = 'medias'
    lesson = Lesson.objects.get(pk=lesson_id)
    lesson.delete()
    lesson_directory = os.path.join(root, 'lesson_' + str(lesson_id))
    shutil.rmtree(lesson_directory)
    return redirect('index')
