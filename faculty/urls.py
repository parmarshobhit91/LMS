from django.urls import path
from . views import *

urlpatterns = [
    path('faculty-manage/', manage_faculties_view, name='manage_faculties_view'),
    path('faculty-details/<int:id>/', faculty_details_view, name='faculty_details_view'),
    path('faculty-edit/<int:id>/', edit_faculty_view, name='edit_faculty_view'),
    path('faculty-delete/<int:id>/', delete_faculty_view, name='delete_faculty_view')
]