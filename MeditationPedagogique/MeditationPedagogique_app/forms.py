from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Element, User, Lesson, Type
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.db.models import F

class CustomUserForm(UserCreationForm):
    username = forms.CharField(label='username', min_length=4, max_length=150)
    email = forms.EmailField(label='email', required=True)
    first_name = forms.CharField(label='first name', max_length=50)
    last_name = forms.CharField(label='last name', max_length=50)
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")


    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = get_user_model().objects.filter(username = username)
        if new.count():
            raise forms.ValidationError("User Already Exist")
        return username


    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = get_user_model().objects.filter(email=email)
        if new.count():
            raise forms.ValidationError("Email Already Exist")
        return email


    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")
        return password2


    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = get_user_model().STUDENT
        if commit:
            user.save()
        return user

class createLessonForm(ModelForm):
    title = forms.CharField(label='Titre', max_length=255)
    class Meta:
        model = Lesson
        fields = ('title',)

    def clean_title(self):
        title = self.cleaned_data['title']
        new = Lesson.objects.filter(title=title)
        if new.count():
            raise forms.ValidationError("Ce titre a déjà été donné à une autre leçon")
        return title

class AddParagraphForm(ModelForm):
    text = forms.CharField(label='Paragraphe', widget=forms.Textarea)

    class Meta:
        model = Element
        fields = ('text',)

    def save(self, lesson_number, order, commit=True):
        order += 1
        paragraph = super(AddParagraphForm, self).save(commit=False)
        paragraph.type = Type.objects.get(name='paragraph')
        paragraph.lesson = Lesson.objects.get(id=lesson_number)
        paragraph.order = order
        paragraph.text = self.cleaned_data['text']
        if commit:
            Element.objects.filter(order__gte=order).update(order = F('order') + 1)
            paragraph.save()
        return paragraph
