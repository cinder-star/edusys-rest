from django.urls import path
from . import views

urlpatterns = [
    path("record/", views.record_attendance, name="record_attendance"),
    path("get_classrooms/",views.get_all_classrooms, name="classrooms"),
    path("activate/",views.activate,name="activate"),
    path("deactivate/",views.deactivate,name="deactivate"),
]