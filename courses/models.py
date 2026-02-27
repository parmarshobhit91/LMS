from django.db import models

# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_duration = models.CharField(max_length=100)
    description = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course_name
    
class Subject(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.Case,
        related_name='subjects'
    )
    subject_name = models.CharField(max_length=100)
    subject_duration = models.CharField(blank=True)

    def __str__(self):
        return f"{self.subject_name} - {self.course.course_name}"