from django.db import models

# Create your models here.
class Student(models.Model):
    class Meta:
        db_table = "student"

    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=254, blank=False)
    contact_no = models.CharField(max_length=14, blank=False)

    def __str__(self):
        return "id: {}\nname: {}\nemail: {}\ncontact: {}\n".format(
            self.id, self.name, self.email, self.contact_no
        )


class Teacher(models.Model):
    class Meta:
        db_table = "teacher"

    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=254, blank=False, unique=True)

    def __str__(self):
        return "id: {}\nname: {}\nemail: {}\n".format(self.id, self.name, self.email)


class Institution(models.Model):
    class Meta:
        db_table = "institution"

    name = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return "id: {}\nname: {}\n".format(self.id, self.name)


class Classroom(models.Model):
    class Meta:
        db_table = "classroom"
        indexes = [
            models.Index(fields=["teacher",]),
        ]

    name = models.CharField(max_length=20, blank=False)
    section = models.CharField(max_length=20)
    teacher = models.ForeignKey(Teacher, to_field="id", on_delete=models.CASCADE)
    institution = models.ForeignKey(
        Institution, to_field="id", on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return "id: {}\nname: {}\nsection: {}\nteacher: {}\n".format(
            self.id, self.name, self.section, str(self.teacher)
        )


class Enrollment(models.Model):
    class Meta:
        db_table = "enrollment"
        indexes = [
            models.Index(fields=["cid", "sid"]),
        ]

    rfid = models.CharField(max_length=8, blank=False, primary_key=True)
    sid = models.ForeignKey(Student, on_delete=models.CASCADE)
    cid = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    roll = models.CharField(max_length=11, blank=False)

    def __str__(self):
        return "rfid: {}\nsid: {}\ncid: {}\nroll: {}\n".format(
            self.rid, str(self.sid), str(self.cid), self.roll
        )


class Attendance(models.Model):
    rfid = models.IntegerField(blank=False)
    cid = models.IntegerField(blank=False, db_index=True)
    date = models.DateField(["%d-%m-%Y"])

    def __str__(self):
        return "rfid: {}\ncid: {}\ndate: {}\n".format(
            self.rfid, str(self.cid), str(self.date)
        )

    class Meta:
        db_table = "attendance"
        indexes = [
            models.Index(fields=["cid",]),
        ]
        unique_together = [
            ["rfid", "date"],
        ]
