from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("record_attendance/", views.record_attendance, name="record_attendance"),
]
