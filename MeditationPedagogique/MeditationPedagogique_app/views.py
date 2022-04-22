from django.shortcuts import render, redirect
from .forms import CustomUserForm, createLessonForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse
from django.apps import apps
import os
import shutil
import datetime
from .models import Lesson, Element, Ressource, Type, GeneralInformation


# Create your views here.
def index(request):
    print(request)

    #Form to get title of new lesson

    context = {}
    context['showForm'] = "False"

    if request.method == 'POST':
        form = createLessonForm(request.POST)
        if form.is_valid():
            title=form['title'].value()
            form.save()
            messages.success(request, 'Creation of lesson successful.')
            lessonDB = Lesson.objects.get(title=title)
            return redirect("lesson/"+str(lessonDB.id))
        else:
            context['showForm'] = "True"
    else:
        form = createLessonForm()
        
    context['form'] = form

    # Get all lectures in the DB
    context['lessonList'] = Lesson.objects.all()
    nbObjects = GeneralInformation.objects.all().count()
    if nbObjects == 0:
        GeneralInformation.objects.create(title="Titre général", description="Description du cours")
    context['generalTitle'] = GeneralInformation.objects.all()[0].title
    context['generalDescription'] = GeneralInformation.objects.all()[0].description

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
    context['ressources'] = Ressource.objects.filter(lesson=number)
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


def delete_lesson(request, lesson_id):
    root = 'medias'
    lesson = Lesson.objects.get(pk=lesson_id)
    lesson.delete()
    lesson_directory = os.path.join(root, 'lesson_' + str(lesson_id))
    shutil.rmtree(lesson_directory)
    return redirect('index')


@login_required
def import_data(request):
    """
    Import file passed by POST method, saving it in appropriate folder and creating a Ressource object in DB
    """
    if request.method == 'POST':
        accepted_format_dictionnary = ['png', 'jpg', 'pdf']
        homework = request.FILES['homework']
        lesson = request.POST.get('lessonNb', '')
        if str(homework).split('.')[-1].lower() in accepted_format_dictionnary:
            # Get slug of the lesson
            lesson_object = Lesson.objects.get(id=lesson).slug
            # Save file in appropriate folder
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, lesson_object))
            filename = fs.save(homework.name, homework)
            request.session['upload_success'] = True
            request.session['uploaded_file_url'] = filename
            
            # Create Ressource element in DB
            ressource = Ressource(user = request.user, path = os.path.join(os.path.join(settings.MEDIA_ROOT, lesson_object), filename), lesson = lesson, date = datetime.datetime.now())
            ressource.save()

            return redirect('lesson', lesson)
        
        # If somehow we receive a file that does not correspond to the define extensions
        request.session['upload_success'] = False
        return redirect('lesson', lesson)

    # If the request is not POST the user is redirected to the index
    return redirect('index')


def update_data(request):
    if request.method == 'POST':
        content = request.POST['content']
        table = request.POST['table']
        id = int(request.POST['id'])
        field = request.POST['field']
        model = apps.get_model(app_label='MeditationPedagogique_app', model_name=table)
        entry = model.objects.all()[id]
        setattr(entry, field, content)
        entry.save(update_fields=[field])

    return HttpResponse('Modification done !')
    #return HttpResponse(response, mimetype='application/json')
