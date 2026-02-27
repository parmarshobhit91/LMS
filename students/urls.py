from django.urls import path
from . views import *

urlpatterns = [
    path('student_dashboard/', student_dashboard_view, name='student_dashboard_view')
]