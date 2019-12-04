from django.db import models

# Create your models here.


class StudentsData(models.Model):
    class Meta:
        db_table = "attendance_studentsdata"

    uid = models.CharField(max_length=15, blank=False, primary_key=True)
    name = models.CharField(max_length=130, blank=False)
    roll = models.CharField(max_length=50, blank=False)
    section = models.CharField(max_length=30, blank=False)
    classno = models.CharField(max_length=20, blank=False)
    email = models.EmailField(blank=True)
    contact_no = models.CharField(max_length=14, blank=False)
    password_hash = models.CharField(max_length=130, blank=False)

    def __str__(self):
        return "UID: {}\r\nName: {}\r\nRoll: {}\r\nClass: {}\r\nSection: {}\r\nEmail: {}\r\nContact no: {}\r\n".format(
            self.uid,
            self.name,
            self.roll,
            self.classno,
            self.section,
            self.email,
            self.contact_no,
        )
