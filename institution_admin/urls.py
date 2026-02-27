from django.urls import path
from . views import *

urlpatterns = [
    path('institution_dashboard/', institution_dashboard_view, name='institution_dashboard_view'),
    path('manage_students/', manage_students_view, name='admin_manage_students_view'),
    path(
        "generate-certificate/<str:enrollment_id>/",
        generate_certificate_view,
        name="generate_certificate_view"
    ),
    path(
        "delete-student/<str:enrollment_id>/",
        delete_student_view,
        name="delete_student_view"
    ),
    path(
        "update-student/<str:enrollment_id>/",
        edit_student_view,
        name="edit_student_view"
    )
]