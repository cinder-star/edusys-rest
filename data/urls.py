from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("all_students/", views.all, name="all_students"),
]
