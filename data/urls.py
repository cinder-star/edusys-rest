from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("add_students/", views.add_students, name="add_students"),
    path("add_teachers/", views.add_teachers, name="add_teachers"),
    path("add_classrooms/", views.add_classrooms, name="add_classrooms"),
    path("add_enrollments/", views.add_enrollments, name="add_enrollments"),
    path("add_attendance/", views.add_attendance, name="add_attendance"),
    path("record_attendance/", views.record, name="record_attendance"),
]
