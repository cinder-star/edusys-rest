from django.db import models


class Enrollment(models.Model):
    class Meta:
        db_table = "enrollment"
        indexes = [
            models.Index(fields=["cid_id", "sid_id"]),
        ]

    rfid = models.CharField(max_length=8, blank=False, primary_key=True)
    sid_id = models.IntegerField(blank=False)
    cid_id = models.IntegerField(blank=False)
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
