from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView

urlpatterns = [
    path('', views.index, name='index'),
    path('inscription/', views.register_request, name='register'),
    path('change-password/', PasswordChangeView.as_view(template_name='registration/change_password.html'), name='password_change'),
    path('change-password-success/', PasswordChangeDoneView.as_view(template_name='registration/change_password_success.html'), name='password_change_done'),
    path('lesson/<int:number>', views.lesson, name='lesson'),
    path('delete_paragraph/', views.delete_paragraph, name='delete_paragraph'),
    path('delete_lesson/<lesson_id>', views.delete_lesson, name='delete-lesson'),
    path('import-data/', views.import_data, name='import_data'),
    path('update-data/', views.update_data, name='update-data'),
    path('add-comment/', views.add_comment, name='add_comment'),
]
