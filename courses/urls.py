from django.urls import path
from . views import *

urlpatterns = [
    path('course/list/', course_list_view, name='course_list_view'),
    path('course/add/', add_course_view, name='add_course_view'),
    path('course/edit/<str:id>/', edit_course_view, name='edit_course_view'),
    path('course/detail/<str:id>/', course_detail_view, name='course_detail_view'),
    path('course/add-subject/', add_subject_view, name='add_subject_view'),
    path('course/<int:course_id>/link-subjects/', link_subject_view, name='link_subject_view'),
    path('course/delete/<str:id>/', delete_course_view, name='delete_course_view'),
    path('course/delete-subject/<str:id>/', delete_subject_view, name='delete_subject_view')
]