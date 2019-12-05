from django.shortcuts import render
from django.http import HttpResponseNotFound, JsonResponse, HttpResponse
from .serializers import JSONSerializer
from .models import StudentsData
import json

# Create your views here.

def find(request):
    uid = request.GET['uid']
    try:
        student = StudentsData.objects.get(uid=uid)
    except:
        return HttpResponseNotFound()

    return HttpResponse()

def all(request):
    try:
        studentsdata = StudentsData.objects.all()
    except:
        return HttpResponseNotFound()
    serializers = JSONSerializer()
    students = serializers.serialize(studentsdata)
    return JsonResponse(students, safe=False)
