from django.shortcuts import render, redirect
from .forms import CustomUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import os
from .models import Lesson, Element, Type


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
    root = 'medias'
    next_lesson_number = len(os.listdir(root))
    medias_directory_name = os.path.join(
        root, 'lesson_' + str(next_lesson_number))
    os.makedirs(medias_directory_name, exist_ok=True)
    lessonDB = Lesson(title='Lesson title')
    lessonDB.save()

    return lesson(request, next_lesson_number)


@login_required
def import_data(request):
    if request.method == 'POST':
        accepted_format_dictionnary = ['png', 'jpg', 'pdf']
        homework = request.FILES['homework']
        if str(homework).split('.')[-1].lower() in accepted_format_dictionnary:
            fs = FileSystemStorage()
            filename = fs.save(homework.name, homework)
            uploaded_file_url = fs.url(filename)
            return redirect('lesson')
        else:
            text_to_return = {'text': 'Le format n\'est pas correct'}
    return render(request, 'forms/import/import_data.html', text_to_return)
