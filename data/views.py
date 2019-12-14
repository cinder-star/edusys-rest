import random
from datetime import date
from django.shortcuts import render
from .random import randomString, hash, random_date
from .models import Student, Teacher, Classroom, Enrollment, Attendance
from django.http import HttpResponseNotFound, JsonResponse, HttpResponse
from .serializers import JSONSerializer
import json

# Create your views here.


def add_students(request):
    for i in range(1000):
        student = Student(
            name=randomString(10), email=randomString(10), contact_no=randomString(10)
        )
        student.save()
    return HttpResponse()


def add_teachers(request):
    for i in range(250):
        teacher = Teacher(name=randomString(10), email=randomString(10))
        teacher.save()
    return HttpResponse()


def add_classrooms(request):
    teachers = list(Teacher.objects.all())
    for i in range(250):
        teachers[i].classroom_set.create(name=randomString(10), section=randomString(5))
        teachers[i].classroom_set.create(name=randomString(10), section=randomString(5))
    return HttpResponse()


def add_enrollments(request):
    students = list(Student.objects.all())
    for i in range(1000):
        x = random.sample(range(1, 500), 2)
        students[i].enrollment_set.create(rfid=str(2 * i), cid_id=x[0], roll=5)
        students[i].enrollment_set.create(rfid=str(2 * i + 1), cid_id=x[1], roll=5)
    return HttpResponse()


def add_attendance(request):
    for i in range(5000):
        x = str(random.randint(1, 1000))
        y = Enrollment.objects.get(rfid=x).cid_id
        attendance = Attendance(rfid=x, cid=y, date=random_date())
        attendance.save()
    return HttpResponse()


def record(request):
    rfid = request.GET["rfid"]
    try:
        student = Enrollment.objects.get(rfid=rfid)
        attendance = Attendance(rfid=rfid, cid=student.cid_id, date=date.today())
        attendance.save(force_insert=True)
    except:
        return HttpResponseNotFound()
    return HttpResponse()
