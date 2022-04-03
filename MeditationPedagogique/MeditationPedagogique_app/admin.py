from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Ressource, Comment, Question, Answer


@admin.register(User)
class UserAdmin(BaseUserAdmin):

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
                    'date', 'is_text', 'text', 'audio_path']


admin.register(Comment, CommentAdmin)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'lesson', 'text']


admin.register(Question, QuestionAdmin)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'question', 'date', 'answer']


admin.register(Answer, AnswerAdmin)
