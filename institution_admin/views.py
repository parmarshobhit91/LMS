from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from students.models import StudentProfile, StudentCourseEnrollment
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
            user__username__icontains=search_query,
            user__email__icontains=search_query,
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

    # Get all courses the student is enrolled in
    enrolled_courses = student.course_enrolled.all()

    certificates = []
    for idx, course in enumerate(enrolled_courses, start=1):
        certificates.append({
            'student_first_name': student.user.first_name,
            'student_last_name': student.user.last_name,
            'course_name': course.course_name,
            'certificate_id': f"CERT-{student.id:05d}-{idx}",
            'completion_date': course.created_at.date() if hasattr(course, 'created_at') else 'N/A',
        })

    context = {
        'certificates': certificates
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
    # Get the student profile
    student = get_object_or_404(StudentProfile, enrollment_number=enrollment_id)

    # Get all courses
    courses = Course.objects.all()

    # IDs of currently enrolled courses
    enrolled_ids = student.course_enrolled.values_list('id', flat=True)

    # Check role
    if request.user.role.lower() not in ['admin', 'faculty']:
        return redirect('home_view')

    if request.method == "POST":
        # --- Update user fields ---
        student.user.first_name = request.POST.get('first_name', student.user.first_name)
        student.user.last_name = request.POST.get('last_name', student.user.last_name)
        student.user.email = request.POST.get('email', student.user.email)
        student.user.username = request.POST.get('username', student.user.username)
        student.user.phone_number = request.POST.get('phone_number', student.user.phone_number)

        profile_image = request.FILES.get('profile_image')
        if profile_image:
            student.user.profile_image = profile_image

        # --- Active / Verified field ---
        is_active = request.POST.get('active')
        if is_active in ['True', 'False']:
            student.user.is_verified = (is_active == 'True')

        # --- Handle course enrollments ---
        course_ids = request.POST.getlist('courses')  # checkbox names = "courses"
        # Remove old enrollments
        StudentCourseEnrollment.objects.filter(student=student).delete()

        if course_ids:
            selected_courses = Course.objects.filter(id__in=course_ids)
            enrollments = [
                StudentCourseEnrollment(student=student, course=c)
                for c in selected_courses
            ]
            StudentCourseEnrollment.objects.bulk_create(enrollments)

        # Save changes
        student.user.save()
        student.save()

        return redirect('admin_manage_students_view')

    # Render the edit form
    return render(request, 'edit_student.html', {
        'student': student,
        'courses': courses,
        'enrolled_ids': enrolled_ids
    })

@login_required
@user_passes_test(is_institution_admin)
def student_details_view(request, enrollment_id):
    student = get_object_or_404(StudentProfile, enrollment_number=enrollment_id)
    context = {
        'student' : student
    }
    return render(request, 'student_details.html', context)