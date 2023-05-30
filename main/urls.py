# django_project/django_website/main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("about", views.aboutpage, name="aboutpage"),
]