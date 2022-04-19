from django.shortcuts import render, redirect
from .forms import CustomUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import datetime
from .models import Lesson, Element, Ressource, Type


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
    context = {
        'upload_success': '',
        'uploaded_file_url': '',
    }
    lessonNumber = Lesson.objects.get(id=number)
    elements =  Element.objects.filter(lesson=lessonNumber)
    if 'upload_success' in request.session:
        context['upload_success'] = request.session['upload_success']
        del request.session['upload_success']
    if 'uploaded_file_url' in request.session:
        context['uploaded_file_url'] = request.session['uploaded_file_url']
        del request.session['uploaded_file_url']
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
        lesson = request.POST.get('lessonNb', '')
        if str(homework).split('.')[-1].lower() in accepted_format_dictionnary:
            lesson_object = Lesson.objects.get(id=lesson).slug
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, lesson_object))
            filename = fs.save(homework.name, homework)
            request.session['upload_success'] = True
            request.session['uploaded_file_url'] = filename
            
            ressource = Ressource(user = request.user, path = os.path.join(os.path.join(settings.MEDIA_ROOT, lesson_object), filename), lesson = lesson, date = datetime.datetime.now())
            ressource.save()

            return redirect('lesson', lesson)
        
        request.session['upload_success'] = False
        return redirect('lesson', lesson)

    return redirect('index')
