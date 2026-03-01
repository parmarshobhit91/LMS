from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from students.models import StudentProfile
from faculty.models import FacultyProfile
from courses.models import Course
from accounts.models import User

# Create your views here.

def is_institution_admin(user):
    return user.role == 'admin'


@login_required
@user_passes_test(is_institution_admin)
def institution_dashboard_view(request):
    student_count = StudentProfile.objects.all().count()
    faculty_count = FacultyProfile.objects.all().count()
    courses_count = Course.objects.all().count()
    all_user_count = User.objects.all().count()
    context = {
        'student_count' : student_count,
        'faculty_count' : faculty_count,
        'courses_count' : courses_count,
        'active_count' : all_user_count,
    }
    return render(request, 'institution_admin.html', context)

@login_required
@user_passes_test(is_institution_admin)
def manage_students_view(request):
    students = StudentProfile.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        students = students.filter(
            user__username__icontains=search_query
        )
    context = {
        'students' : students
    }
    return render(request, 'manage_students.html', context)


@login_required
@user_passes_test(is_institution_admin)
def generate_certificate_view(request, enrollment_id):
    student = get_object_or_404(StudentProfile, enrollment_number=enrollment_id)

    if request.user.role not in ['admin', 'faculty', 'Admin', 'Faculty']:
        return redirect('home_view')
    
    context = {
        'student_first_name' : student.user.first_name,
        'student_last_name' : student.user.last_name,
        'course_name' : student.course_enrolled,
        'certificate_id' : f"CERT-{student.id:05d}"
    }

    return render(request, "certificate_template.html", context)


@login_required
@user_passes_test(is_institution_admin)
def delete_student_view(request, enrollment_id):
    student = get_object_or_404(StudentProfile, enrollment_number=enrollment_id)

    if request.user.role not in ['admin', 'faculty', 'Admin', 'Faculty']:
        return redirect('home_view')
    
    student.user.delete()
    return redirect('admin_manage_students_view')

@login_required
@user_passes_test(is_institution_admin)
def edit_student_view(request, enrollment_id):
    student = get_object_or_404(StudentProfile, enrollment_number=enrollment_id)
    # student = StudentProfile.objects.select_for_update().get(enrollment_number=enrollment_id)

    if request.user.role not in ['admin', 'faculty', 'Admin', 'Faculty']:
        return redirect('home_view')
    
    if request.method == "POST":
        firstname = request.POST.get('first_name')
        if firstname:
            student.user.first_name = firstname

        lastname = request.POST.get('last_name')
        if lastname:
            student.user.last_name = lastname

        email = request.POST.get('email')
        if email:
            student.user.email = email

        phone_number = request.POST.get('phone_number')
        if phone_number:
            student.user.phone_number = phone_number

        course_enrolled = request.POST.get('course_enrolled')
        if course_enrolled:
            student.course_enrolled = course_enrolled

        username = request.POST.get('username')
        if username:
            student.user.username = username

        is_active = request.POST.get('active')
        if is_active:
            student.user.is_verified = is_active


        student.user.save()
        student.save()
        return redirect('admin_manage_students_view')
    return render(request, 'edit_student.html')

@login_required
@user_passes_test(is_institution_admin)
def student_details_view(request, enrollment_id):
    student = get_object_or_404(StudentProfile, enrollment_number=enrollment_id)
    context = {
        'student' : student
    }
    return render(request, 'student_details.html', context)