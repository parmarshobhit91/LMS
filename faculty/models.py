from django.db import models
from django.conf import settings
from courses.models import Subject

# Create your models here.

class FacultyProfile(models.Model):

    ROLE_CHOICES = (
        ('instructor', 'Instructor'),
        ('hod', 'Hod'),
        ('admissions_officer', 'Admissions_officer'),
        ('finance_officer', 'Finance_officer'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='faculty_profile'
    )

    employee_id = models.CharField(max_length=50, unique=True)

    aadhar_number = models.CharField(max_length=50, unique=True, null=True, blank=True)

    qualification = models.CharField(max_length=200, null=True, blank=True)
    specialization = models.CharField(max_length=200, null=True, blank=True)

    faculty_role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='instructor')

    experience_years = models.PositiveIntegerField(null=True, blank=True)

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    joining_date = models.DateField(null=True, blank=True)

    address = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    subjects = models.ManyToManyField(
        Subject,
        related_name='faculties',
        blank=True
    )

    def __str__(self):
        return f"Faculty: {self.user.email}"