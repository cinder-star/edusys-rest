from django.shortcuts import render
from django.http import Http404, JsonResponse
from .serializers import JSONSerializer
from .models import StudentsData
import json

# Create your views here.


def all(request):
    try:
        studentsdata = StudentsData.objects.all()
    except:
        raise Http404("Not found")
    serializers = JSONSerializer()
    students = serializers.serialize(studentsdata)
    return JsonResponse(students, safe=False)
