from django.shortcuts import render
from django.http import HttpResponseNotFound, JsonResponse, HttpResponse
from .serializers import JSONSerializer
from .models import StudentsData
import json

# Create your views here.

def find(request):
    uid = request.GET['uid']
    if StudentsData.objects.filter(uid=uid).exists():
        return HttpResponse()
    return HttpResponseNotFound()

def add(request, uid, student_name, email, contact_no, roll, section, class_no):
    student = StudentsData(
        uid=uid,
        name=student_name,
        roll=roll,
        section=section,
        classno=class_no,
        email=email,
        contact_no=contact_no,
        password_hash="abcdef",
    )
    try:
        student.save(force_insert=True)
    except:
        raise HttpResponseNotFound()
    return HttpResponse()

def all(request):
    try:
        studentsdata = StudentsData.objects.all()
    except:
        return HttpResponseNotFound()
    serializers = JSONSerializer()
    students = serializers.serialize(studentsdata)
    return JsonResponse(students, safe=False)
