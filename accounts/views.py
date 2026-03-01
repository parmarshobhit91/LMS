from django.shortcuts import render, redirect
from . models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from students.models import StudentProfile
from faculty.models import FacultyProfile

# Create your views here.
def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    return render(request, 'register.html')

def faculty_register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        username = request.POST.get('username')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('faculty_register_view')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('faculty_register_view')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match. Try again!")
            return redirect('faculty_register_view')
    
        if " " in username:
            messages.error(request, "Username cannot contain spaces!")
            return redirect('student_register_view')

        if " " in password:
            messages.error(request, "Password cannot contain spaces!")
            return redirect('student_register_view')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone_number = phone_number,
            first_name = first_name,
            last_name = last_name,
            role='faculty'
        )

        user2 = FacultyProfile.objects.create(
            user = user,
            employee_id = request.POST.get('employee_id'),
            aadhar_number = request.POST.get('aadhar_number'),
            qualification = request.POST.get('qualification'),
            specialization = request.POST.get('specialization'),
            faculty_role = request.POST.get('faculty_role'),
            experience_years = request.POST.get('experience_years'),
            salary = request.POST.get('salary'),
            joining_date = request.POST.get('joining_date'),
            address = request.POST.get('address')
        )

        messages.success(request, "Registration successful ! Please login to continue...")
        if request.user.role == 'admin':
            return redirect('manage_faculties_view')
    return render(request, 'faculty-register.html')

def student_register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        username = request.POST.get('username')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        enrollment_id = request.POST.get('enrollment_id')
        course_name = request.POST.get('course_name')
        academic_year = request.POST.get('academic_year')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('student_register_view')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('student_register_view')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match. Try again!")
            return redirect('student_register_view')
        
        if " " in username:
            messages.error(request, "Username cannot contain spaces!")
            return redirect('student_register_view')

        if " " in password:
            messages.error(request, "Password cannot contain spaces!")
            return redirect('student_register_view')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone_number = phone_number,
            first_name = first_name,
            last_name = last_name,
            role='student'
        )

        user2 = StudentProfile.objects.create(
            user = user,
            enrollment_number = enrollment_id,
            course_enrolled = course_name,
            academic_year = academic_year
        )

        messages.success(request, "Registration successful ! Please login to continue...")

        if request.user.role == 'admin':
            return redirect('admin_manage_students_view')
        else:
            return redirect('faculty_manage_students_view')
    return render(request, 'student-register.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None and user.role == 'student':
                login(request, user)
                return redirect('student_dashboard_view')
                # return HttpResponse("User logged in.")
            elif user.role == 'faculty':
                login(request, user)
                return redirect('faculty_dashboard_view')
            elif user.role == 'admin':
                login(request, user)
                return redirect('institution_dashboard_view')
            else:
                messages.error(request, "Invalid credentials!")
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials!")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)   # This clears the session
    return redirect('login_view')  # redirect to login page