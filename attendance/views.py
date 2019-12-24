from pytz import utc, timezone
from datetime import datetime
from .models import User, Classroom, Enrollment, Attendance
from django.http import HttpResponseNotFound, JsonResponse, HttpResponse
from .serializers import JSONSerializer
import json

def record_attendance(request):
    rfid = request.GET["rfid"]
    date = request.GET["date"]
    time = request.GET["time"]
    utc_now = utc.localize(datetime.utcnow())
    server_time = utc_now.astimezone(timezone("Asia/Dhaka"))
    entry_date = server_time.strftime("%Y-%m-%d")
    entry_time = server_time.strftime("%H:%M:%S")
    try:
        student = Enrollment.objects.get(rfid=rfid)
        if not student.active:
            raise Exception()
        attendance = Attendance(
            rfid=rfid,
            cid=student.cid_id,
            punch_time=time,
            punch_date=date,
            entry_date=entry_date,
            entry_time=entry_time,
        )
        attendance.save()
    except:
        return HttpResponseNotFound()
    return HttpResponse()

def get_all_classrooms(request):
    try:
        rfid=request.GET["rfid"]
        classrooms = list(Classroom.objects.filter(punch_id_id=rfid).only('id','name','section'))
        serializers = JSONSerializer()
        classes = serializers.serialize(classrooms)
        return JsonResponse(classes, safe=False)
    except:
        return HttpResponseNotFound()

def activate(request):
    try:
        rfid=request.GET["rfid"]
        class_id=request.GET["class_id"]
        classroom=Classroom.objects.get(id=class_id,punch_id_id=rfid)
        Enrollment.objects.filter(cid_id=class_id).update(active=True)
        return HttpResponse()
    except:
        return HttpResponseNotFound()

def deactivate(request):
    try:
        rfid=request.GET["rfid"]
        class_id=request.GET["class_id"]
        classroom=Classroom.objects.get(id=class_id,punch_id_id=rfid)
        Enrollment.objects.filter(cid_id=class_id).update(active=False)
        return HttpResponse()
    except:
        return HttpResponseNotFound()