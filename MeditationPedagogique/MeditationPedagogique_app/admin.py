from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserForm
from .models import User, Ressource, Comment, Question, Answer, Type, Lesson, Element, GeneralInformation, InscriptionCode

@admin.register(User)
class UserAdmin(BaseUserAdmin):

    add_form = CustomUserForm

    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password', 'role')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ['username', 'email', 'first_name',
                    'last_name', 'role', 'is_active', 'is_staff']

    def __init__(self, *args, **kwargs):
        super(BaseUserAdmin, self).__init__(*args, **kwargs)
        BaseUserAdmin.list_display = list(BaseUserAdmin.list_display)


admin.register(UserAdmin)


@admin.register(Ressource)
class RessourceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'path', 'lesson',
                    'title', 'description', 'date']


admin.register(Ressource, RessourceAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ressource',
                    'date', 'text']


admin.register(Comment, CommentAdmin)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'evaluation', 'text', 'type']


admin.register(Question, QuestionAdmin)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'question', 'date', 'answerNumber', 'answerText']


admin.register(Answer, AnswerAdmin)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.register(Type, TypeAdmin)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']


admin.register(Lesson, LessonAdmin)


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'lesson', 'order', 'path', 'text']


admin.register(Element, ElementAdmin)

@admin.register(GeneralInformation)
class GeneralInformationsAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']


admin.register(GeneralInformation, GeneralInformationsAdmin)


@admin.register(InscriptionCode)
class InscriptionCodesAdmin(admin.ModelAdmin):
    list_display = ['role', 'code']


admin.register(InscriptionCode, InscriptionCodesAdmin)
