from django.urls import path
from . views import *

urlpatterns = [
    path('', home_view, name='home_view'),
    path('register/', register_view, name='register_view'),
    path('register/faculty/', faculty_register_view, name='faculty_register_view'),
    path('register/student/', student_register_view, name='student_register_view'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),

]