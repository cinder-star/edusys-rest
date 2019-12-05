from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("all_students/", views.all, name="all_students"),
    path("find_student/",views.find,name="find_student"),
    path(
        "add_student/<str:uid>/<str:student_name>/<str:roll>/<str:section>/<str:class_no>/<str:email>/<str:contact_no>/",
        views.add,
        name="add_student",
    ),
]
