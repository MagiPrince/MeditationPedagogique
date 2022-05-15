from django.shortcuts import render, redirect
from .forms import CustomUserForm, createLessonForm, AddParagraphForm, CreateEvaluationForm, CreateQuestionForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse
from django.apps import apps
from django.utils import timezone
import os
import datetime
from .models import Lesson, Element, Ressource, Type, GeneralInformation, Comment, User, Question, Answer, InscriptionCode
import operator
from django.db.models import F


# Create your views here.
def index(request):
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
        'upload_success_element': '',
        'uploaded_file_url_element': '',
        'modalID': '',
    }
    lessonNumber = Lesson.objects.get(id=number)
    elements =  Element.objects.filter(lesson=lessonNumber)
    if 'upload_success' in request.session:
        context['upload_success'] = request.session['upload_success']
        del request.session['upload_success']
    if 'uploaded_file_url' in request.session:
        context['uploaded_file_url'] = request.session['uploaded_file_url']
        del request.session['uploaded_file_url']

    if 'upload_success_element' in request.session:
        context['upload_success_element'] = request.session['upload_success_element']
        del request.session['upload_success_element']
    if 'uploaded_file_url_element' in request.session:
        context['uploaded_file_url_element'] = request.session['uploaded_file_url_element']
        del request.session['uploaded_file_url_element']

    context = {}
    context['showForm'] = "False"
    context['showUpdateModal'] = "False"
    if 'paragraphButton' in request.POST:
        types_created_verification()
        form = AddParagraphForm(request.POST)
        order = int(request.POST.get('add_element_order', ''))
        if form.is_valid():
            form.save(lesson_number=number, order=order)
            messages.success(request, 'Creation of lesson successful.')
            return redirect('/lesson/' + str(lessonNumber.id))
        else:
            context['showForm'] = "True"
            context['form'] = form

    elif 'evaluationButton' in request.POST:
        types_created_verification()
        createEvaluationForm = CreateEvaluationForm(request.POST)
        order = int(request.POST.get('add_element_order', ''))
        if createEvaluationForm.is_valid():
            createEvaluationForm.save(lesson_number=number, order=order)
            return redirect('/lesson/' + str(lessonNumber.id))
        else:
            context['createEvaluationForm'] = createEvaluationForm

    elif 'questionButton' in request.POST:
        elementId = int(request.POST.get('elementId', ''))
        createQuestionForm = CreateQuestionForm(request.POST)
        if createQuestionForm.is_valid():
            createQuestionForm.save(elementId=elementId)
            return redirect('/lesson/' + str(lessonNumber.id))
        else:
            context['createQuestionForm'] = createQuestionForm
    elif 'answerButton' in request.POST:
        evaluationId = int(request.POST.get('elementId', ''))
        element = Element.objects.get(pk=evaluationId)
        user_answerer = request.user
        questionIds = element.question_of_evaluation.all().values('id')
        changes = False
        for questionId in questionIds:
            answer = request.POST.get('question'+str(questionId['id']), '')
            question = Question.objects.get(pk=questionId['id'])

            #Check if user already answered this question or not:
            previousAnswer = question.answer_of_question.all().filter(user=user_answerer).first()
            if question.type==1:
                if previousAnswer != None:
                    if previousAnswer.answerText != answer:
                        changes = True
                else:
                    if answer!='':
                        changes = True
                if answer=='' and previousAnswer != None:
                    previousAnswer.delete()
                elif answer!='':
                    answerElement, created = Answer.objects.update_or_create(
                    user=user_answerer, question=question,
                    defaults={'date': timezone.now(), 'answerText': answer}
                    )
            elif question.type==2:
                if answer != "-1":
                    if previousAnswer != None:
                        if str(previousAnswer.answerNumber) != str(answer):
                            changes = True
                    else:
                        changes = True
                    answerElement, created = Answer.objects.update_or_create(
                    user=user_answerer, question=question,
                    defaults={'date': timezone.now(), 'answerNumber': answer}
                    )
                else:
                    if previousAnswer != None:
                        previousAnswer.delete()
                        changes = True

        if changes == True:
            context['showUpdateModal'] = "True"
    else:
        form = AddParagraphForm()
        createEvaluationForm = CreateEvaluationForm()
        createQuestionForm = CreateQuestionForm()
        context['form'] = form
        context['createEvaluationForm'] = createEvaluationForm
        context['createQuestionForm'] = createQuestionForm

    context['elements'] = sorted(elements, key=operator.attrgetter('order'))
    context['title'] = Lesson.objects.all().filter(id=number)[0].title
    context['lessonNumber'] = number
    context['ressources'] = Ressource.objects.filter(lesson=number)
    if 'modalId' in request.session:
        context['modalId'] = request.session['modalId']
        del request.session['modalId']
    return render(request, 'lessons/lesson.html', context)

def delete_paragraph(request):
    if request.method == 'POST':
        pargraph_id = int(request.POST.get('delete_element_id', ''))
        order = int(request.POST.get('delete_element_order', ''))
        lessonNumber = int(request.POST.get('lesson_number', ''))
        element = Element.objects.get(pk=pargraph_id)
        element.delete()
        Element.objects.filter(order__gte=order).update(order = F('order') - 1)
        return redirect('/lesson/' + str(lessonNumber))

def delete_lesson(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    lesson.delete()
    return redirect('index')

def delete_question(request):

    if request.method == 'POST':
        questionId = request.POST.get('delete_question_id', '')
        question = Question.objects.get(pk=questionId)
        question.delete()
        lessonNumber = int(request.POST.get('lesson_number', ''))
        return redirect('/lesson/' + str(lessonNumber))

@login_required
def import_data(request):
    """
    Import file passed by POST method, saving it in appropriate folder and creating a Ressource object in DB
    """
    if request.method == 'POST':
        accepted_format_dictionnary = ['png', 'jpg', 'pdf']
        homework = request.FILES['homework']
        lesson = request.POST.get('lessonNb', '')
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        licence_selected = request.POST.get('licenceSelected', '')
        if str(homework).split('.')[-1].lower() in accepted_format_dictionnary:
            # Get slug of the lesson
            lesson_object = Lesson.objects.get(id=lesson).slug
            # Save file in appropriate folder
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, lesson_object))
            filename = fs.save(homework.name, homework)
            request.session['upload_success'] = True
            request.session['uploaded_file_url'] = filename

            # Create Ressource element in DB
            ressource = Ressource(user = request.user, title=title, description=description, path = os.path.join( lesson_object, filename), lesson = lesson, date = datetime.datetime.now(), licence_selected=licence_selected)
            ressource.save()

            return redirect('lesson', lesson)

        # If somehow we receive a file that does not correspond to the define extensions
        request.session['upload_success'] = False
        return redirect('lesson', lesson)

    # If the request is not POST the user is redirected to the index
    return redirect('index')


@user_passes_test(lambda u: u.is_superuser)
def import_element(request):
    """
    Import file passed by POST method, saving it in appropriate folder and creating a Ressource object in DB
    """
    if request.method == 'POST':
        accepted_format_dictionnary = ['pdf', 'mp3', 'mp4', 'jpg', 'png', 'jpeg', 'gif']
        element = request.FILES['element']
        lesson = request.POST.get('lessonNb', '')
        order = int(request.POST['add_element_order'])
        extension = str(element).split('.')[-1].lower()
        if extension in accepted_format_dictionnary:
            # Get slug of the lesson
            lesson_object = Lesson.objects.get(id=lesson).slug
            # Save file in appropriate folder
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, lesson_object))
            filename = fs.save(element.name, element)
            request.session['upload_success_element'] = True
            request.session['uploaded_file_url_element'] = filename

            types_created_verification()

            # Define Type
            type = ''
            if extension in ['jpg', 'png', 'jpeg', 'gif']:
                type = Type.objects.get(name='image')
            if extension == 'pdf':
                type = Type.objects.get(name='document')
            if extension == 'mp3':
                type = Type.objects.get(name='audio')
            if extension == 'mp4':
                type = Type.objects.get(name='video')

            # Create Element element in DB
            order += 1
            e = Element(type=type, lesson=Lesson.objects.get(id=lesson), order=order, path=os.path.join( lesson_object, filename))
            Element.objects.filter(lesson=Lesson.objects.get(id=lesson), order__gte=order).update(order = F('order') + 1)
            e.save()


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
        entry = model.objects.get(pk=id)
        setattr(entry, field, content)
        entry.save(update_fields=[field])

    return HttpResponse('Modification done !')


@login_required
def add_comment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        ressource = request.POST['ressourceName']
        lesson = request.POST.get('lessonNb', '')
        comment_hidden = bool(request.POST.get('commentHidden', ''))
        if comment_hidden and request.user.is_superuser:
            comment_hidden = True
        else:
            comment_hidden = False
        request.session['modalId'] = request.POST.get('modalId', '')

        c = Comment(user=request.user, ressource=Ressource.objects.get(id=ressource), text=comment, date=datetime.datetime.now(), hidden=comment_hidden)
        c.save()

        if lesson != '':
            return redirect('lesson', lesson)

    # If the request is not POST the user is redirected to the index
    return redirect('index')


@login_required
def delete_comment(request):
    if request.method == 'POST':
        comment_id = request.POST['commentId']
        lesson = request.POST.get('lessonNb', '')
        request.session['modalId'] = request.POST.get('modalId', '')
        if request.user.is_superuser or request.user == User.objects.get(id=Comment.objects.filter(id=comment_id).values('user')[0]['user']):
            Comment.objects.get(id=comment_id).delete()
        return redirect('lesson', lesson)

    # If the request is not POST the user is redirected to the index
    return redirect('index')


def edit(request):
    if request.method == 'POST':
        modification_modal_id = int(request.POST.get('modification_modal_id', ''))
        modification_modal_table = request.POST.get('modification_modal_table', '')
        modification_modal_field = request.POST.get('modification_modal_field', '')
        modification_modal_text = request.POST.get('modification_modal_text', '')
        print(modification_modal_text)
        model = apps.get_model(app_label='MeditationPedagogique_app', model_name=modification_modal_table)
        entry = model.objects.get(pk=modification_modal_id)
        setattr(entry, modification_modal_field, modification_modal_text)
        entry.save(update_fields=[modification_modal_field])

    return redirect(request.META['HTTP_REFERER'])

@login_required
def delete_ressource(request):
    if request.method == 'POST':
        ressource_id = request.POST['ressourceId']
        lesson = request.POST.get('lessonNb', '')

        if request.user.is_superuser or request.user.role == 2 or request.user == User.objects.get(id=Ressource.objects.filter(id=ressource_id).values('user')[0]['user']):
            Ressource.objects.get(id=ressource_id).delete()
        return redirect(request.META['HTTP_REFERER'])

    # If the request is not POST the user is redirected to where he was
    return redirect(request.META['HTTP_REFERER'])

def profile(request, username):
    context= {}
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        context['username'] = user.username
        context['role'] = user.role
        context['ressources'] = Ressource.objects.filter(user=user)
        return render(request, 'profile.html', context)
    else:
        print("We didn't find the user", username)
        return redirect('index')

def types_created_verification():
    # Verify that types for elements are created, if not create them
    if len(Type.objects.all()) < 6:
        print(len(Type.objects.all()))
        if len(Type.objects.filter(name='audio')) < 1:
            t = Type(name='audio')
            t.save()
        if len(Type.objects.filter(name='document')) < 1:
            t = Type(name='document')
            t.save()
        if len(Type.objects.filter(name='image')) < 1:
            t = Type(name='image')
            t.save()
        if len(Type.objects.filter(name='paragraph')) < 1:
            t = Type(name='paragraph')
            t.save()
        if len(Type.objects.filter(name='video')) < 1:
            t = Type(name='video')
            t.save()
        if len(Type.objects.filter(name='evaluation')) < 1:
            t = Type(name='evaluation')
            t.save()

def codes(request):
    context = {}

    if request.user.is_superuser:
        # Get all codes in the DB
        context['studentCodes'] = InscriptionCode.objects.filter(role=1)
        context['profCodes'] = InscriptionCode.objects.filter(role=2)

    return render(request, 'codes.html', context)

@login_required
def delete_code(request):
    if request.method == 'POST':
        code_id = request.POST['code_id']
        if request.user.is_superuser:
            InscriptionCode.objects.get(id=code_id).delete()

    # If the request is not POST the user is redirected to the codes page
    return redirect('codes')

@login_required
def add_code(request):
    if request.method == 'POST':
        code = request.POST['code']
        role = request.POST['role']
        c = InscriptionCode(code=code, role=role)
        c.save()
    # If the request is not POST the user is redirected to the codes page
    return redirect('codes')