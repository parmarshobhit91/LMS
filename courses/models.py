from django.db import models

# Create your models here.
class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_duration = models.CharField(blank=True)

    def __str__(self):
        return f"{self.subject_name}"
    
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_duration = models.CharField(max_length=100)
    description = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    course_fee = models.PositiveIntegerField(blank=True, null=True)

    subjects = models.ManyToManyField(Subject, blank=True)

    def __str__(self):
        return self.course_name
    
class CourseAttendance(models.Model):

    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
    )
    
    student = models.ForeignKey(
        'students.StudentProfile',
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        'faculty.FacultyProfile',
        on_delete=models.CASCADE
    )

    date = models.DateField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'course', 'date')

class SubjectAttendance(models.Model):
    
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
    )

    student = models.ForeignKey(
        'students.StudentProfile',
        on_delete=models.CASCADE
        )
    
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE
    )

    date = models.DateField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'course', 'date')