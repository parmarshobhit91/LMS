from django.contrib import admin
from . models import *

# Register your models here.

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name']

    
