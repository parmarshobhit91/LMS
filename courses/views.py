from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from . models import *

# Create your views here.

def is_institution_admin(user):
    return user.role == 'admin'

@login_required
@user_passes_test(is_institution_admin)
def course_list_view(request):
    courses = Course.objects.all()
    subjects = Subject.objects.all()
    context = {
        'courses' : courses,
        'subjects' : subjects
    }
    return render(request, 'course_list.html', context)

@login_required
@user_passes_test(is_institution_admin)
def add_course_view(request):
    if request.method == "POST":
        course_name = request.POST.get('course_name')
        course_duration = request.POST.get('course_duration')
        course_description = request.POST.get('description')
    
        Course.objects.create(
            course_name = course_name,
            course_duration = course_duration,
            description = course_description
        )
        return redirect('course_list_view')

    return render(request, 'add_course.html')

@login_required
@user_passes_test(is_institution_admin)
def edit_course_view(request, id):
    course = get_object_or_404(Course, id=id)

    if request.method == "POST":
        name = request.POST.get('course_name')
        if name:
            course.course_name = name

        duration = request.POST.get('course_duration')
        if duration:
            course.course_duration = duration

        course_description = request.POST.get('description')
        if course_description:
            course.description = course_description

        course.save()
        return redirect('course_list_view')

    return render(request, 'edit_course.html')

@login_required
@user_passes_test(is_institution_admin)
def course_detail_view(request, id):
    course = get_object_or_404(Course, id=id)
    context = {
        'course': course
    }
    return render(request, 'course_detail.html', context)

@login_required
@user_passes_test(is_institution_admin)
def add_subject_view(request):
    if request.method == "POST":
        Subject.objects.create(
        subject_name = request.POST.get('subject_name'),
        subject_duration = request.POST.get('subject_duration')
    )
        return redirect('course_list_view')
    return render(request, 'add_subject.html')

@login_required
@user_passes_test(is_institution_admin)
def delete_course_view(request, id):
    course = get_object_or_404(Course, id=id)
    course.delete()
    return redirect('course_list_view')

@login_required
@user_passes_test(is_institution_admin)
def delete_subject_view(request, id):
    subject = get_object_or_404(Subject, id=id)
    subject.delete()
    return redirect('course_list_view')

@login_required
@user_passes_test(is_institution_admin)
def link_subject_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    subjects = Subject.objects.all()

    context = {
        'course': course,
        'subjects': subjects
    }

    if request.method == "POST":
        selected_subjects = request.POST.getlist("subjects")
        course.subjects.set(selected_subjects)
        return redirect('course_detail_view', id=course.id)
    
    return render(request, 'link_subject.html', context)