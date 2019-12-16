import random
from datetime import date
from django.db import transaction
from django.shortcuts import render
from .models import Enrollment, Attendance
from .random import randomString, hash, random_date
from django.http import HttpResponseNotFound, JsonResponse, HttpResponse
from .serializers import JSONSerializer
import json

# Create your views here.
@transaction.atomic
def record_attendance(request):
    rfid = request.GET["rfid"]
    try:
        student = Enrollment.objects.get(rfid=rfid)
        attendance = Attendance(rfid=rfid, cid=student.cid_id, date=date.today())
        attendance.save()
    except:
        return HttpResponseNotFound()
    return HttpResponse()
