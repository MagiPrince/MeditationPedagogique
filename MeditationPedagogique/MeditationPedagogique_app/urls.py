from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('inscription', views.register_request, name='register'),
]
