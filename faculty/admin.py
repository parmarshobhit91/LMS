from django.contrib import admin
from . models import FacultyProfile

# Register your models here.
@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'specialization']