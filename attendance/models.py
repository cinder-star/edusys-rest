from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
from datetime import date
from django.core import validators
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(
        self,
        username,
        password,
        full_name,
        is_staff,
        is_superuser,
        role,
        **extra_fields
    ):
        if not username:
            raise ValueError("Users must have an email address")
        now = timezone.now()
        user = self.model(
            username=username,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            full_name=full_name,
            last_login=now,
            date_joined=now,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, username=None, password=None, full_name=None, role=None, **extra_fields
    ):
        return self._create_user(
            username, password, full_name, False, False, role, **extra_fields
        )

    def create_superuser(self, username, password, **extra_fields):
        user = self._create_user(
            username, password, username, True, True, role=4, **extra_fields
        )
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = "user"

    email = models.EmailField(_("Email Address"), unique=False,)
    username = models.CharField(
        _("Username"),
        max_length=30,
        unique=True,
        blank=False,
        null=True,
        help_text=("30 characters or fewer. Letters, digits and _ only."),
        validators=[
            validators.RegexValidator(
                r"^\w+$",
                (
                    "Enter a valid username. This value may contain only "
                    "letters, numbers and _ character."
                ),
                "invalid",
            ),
        ],
        error_messages={"unique": ("The username is already taken."),},
    )
    first_name = models.CharField(_("First Name"), max_length=30, blank=True, null=True)
    last_name = models.CharField(_("Last Name"), max_length=30, blank=True, null=True)
    full_name = models.CharField(
        _("Full Name"),
        max_length=100,
        blank=False,
        null=False,
        unique=False,
        default=None,
    )
    contact_no = models.CharField(
        _("Contact Number"),
        max_length=14,
        blank=False,
        help_text=_("Phone number to contact the person when necessary"),
    )

    STUDENT = 1
    TEACHER = 2
    SCHOOL_ADMIN = 3
    ROLE_CHOICES = (
        (STUDENT, "student"),
        (TEACHER, "teacher"),
        (SCHOOL_ADMIN, "admin"),
    )
    role = models.PositiveSmallIntegerField(
        _("Role"),
        choices=ROLE_CHOICES,
        help_text=_(
            "The user's role in the system. There are three roles: student, teacher and school-administration"
        ),
        blank=False,
        null=False,
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    teacher_rfid = models.CharField(
        _("teacher_rfid"), max_length=8, blank=True, null=True, unique=True
    )
    affiliation = models.ForeignKey(
        "self", to_field="id", on_delete=models.PROTECT, null=True, blank=True
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return "id: {}\nusername: {}\nemail: {}\ncontact: {}\n".format(
            self.id, self.username, self.email, self.contact_no
        )

    def get_username(self):
        return self.username


class Classroom(models.Model):
    class Meta:
        db_table = "classroom"
        indexes = [
            models.Index(fields=["teacher",]),
        ]
        unique_together = [
            ["name", "section", "teacher_id", "institution_id"],
        ]

    name = models.CharField(max_length=20, blank=False)
    section = models.CharField(max_length=20)
    punch_id = models.ForeignKey(
        User, to_field="teacher_rfid", on_delete=models.PROTECT, default=None
    )
    teacher = models.ForeignKey(
        User, to_field="id", related_name="teacher_classroom", on_delete=models.CASCADE
    )
    institution = models.ForeignKey(
        User,
        to_field="id",
        on_delete=models.CASCADE,
        related_name="institution_classroom",
        blank=True,
        null=True,
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
    sid = models.ForeignKey(User, on_delete=models.CASCADE)
    cid = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    roll = models.CharField(max_length=11, blank=False)
    active = models.BooleanField(default=False)

    def __str__(self):
        return "rfid: {}\nsid: {}\ncid: {}\nroll: {}\n".format(
            self.rfid, str(self.sid), str(self.cid), self.roll
        )


class Attendance(models.Model):
    rfid_id = models.CharField(max_length=8, blank=False)
    cid = models.IntegerField(blank=False, db_index=True, db_column="cid_id")
    entry_date = models.CharField(max_length=10, default=None)
    punch_date = models.CharField(max_length=10, default=None)
    entry_time = models.CharField(max_length=8, default=None)
    punch_time = models.CharField(max_length=8, default=None)
    sms_sent = models.BooleanField(default=False)

    def __str__(self):
        return "rfid: {}\ncid: {}\ndate: {}\n".format(
            self.rfid, str(self.cid), self.punch_date
        )

    class Meta:
        db_table = "attendance"
        indexes = [
            models.Index(fields=["cid",]),
        ]
        unique_together = [
            ["rfid_id", "punch_date"],
        ]

    class AffiliationRequest(models.Model):
        request_from = models.ForeignKey(
            User, to_field="id", related_name="teacher", on_delete=models.CASCADE
        )
        request_to = models.OneToOneField(
            User, to_field="id", related_name="institution", on_delete=models.CASCADE
        )

        class Meta:
            unique_together = [
                ["request_from", "request_to"],
            ]
