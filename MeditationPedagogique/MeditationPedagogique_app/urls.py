from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView

urlpatterns=[
    path('', views.index, name='index'),
    path('inscription/', views.register_request, name='register'),
    path('modifier_mdp/', PasswordChangeView.as_view(template_name='registration/change_password.html'), name='password_change'),
    path('modifier_mdp_succes', PasswordChangeDoneView.as_view(template_name='registration/change_password_success.html'), name='password_change_done'),
]
