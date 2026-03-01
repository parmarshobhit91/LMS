from django.db import models
from django.conf import settings
from courses.models import Course

# Create your models here.

class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    enrollment_number = models.CharField(max_length=50, unique=True)
    course_enrolled = models.ManyToManyField(
        Course,
        through='StudentCourseEnrollment',
        related_name='students'
    )
    academic_year = models.CharField(max_length=20)

    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_phone = models.CharField(max_length=15, blank=True, null=True)

    address = models.TextField(blank=True, null=True)

    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Student: {self.user.email}"
    
class StudentCourseEnrollment(models.Model):
    
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE
        )
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    enrolled_on = models.DateField()

    class Meta:
        unique_together = ('student', 'course')