from django.shortcuts import render, get_object_or_404, redirect
from . models import *
from django.core.paginator import Paginator



# Create your views here.

def manage_faculties_view(request):
    faculty_list = FacultyProfile.objects.all()

    search_query = request.GET.get('search')
    if search_query:
        faculty_list = faculty_list.filter(
            user__username__icontains=search_query
        )

    paginator = Paginator(faculty_list, 10)
    page = request.GET.get('page')
    faculties = paginator.get_page(page)

    context = {
        'faculties': faculties
    }
    return render(request, 'manage_faculties.html', context)

def faculty_details_view(request, id):
    faculty = get_object_or_404(FacultyProfile, id=id)
    context = {
        'faculty': faculty
    }
    return render(request, 'faculty_details.html', context)

def edit_faculty_view(request, id):
    faculty = get_object_or_404(FacultyProfile, id=id)
    roles = FacultyProfile.ROLE_CHOICES

    if request.method == "POST":

        faculty.user.first_name = request.POST.get('first_name')
        faculty.user.last_name = request.POST.get('last_name')
        faculty.user.email = request.POST.get('email')
        faculty.user.username = request.POST.get('username')
        faculty.user.phone_number = request.POST.get('phone_number')
        faculty.user.is_verified = request.POST.get('active') == "True"

        faculty.qualification = request.POST.get('qualification')
        faculty.specialization = request.POST.get('specialization')
        faculty.faculty_role = request.POST.get('faculty_role')
        faculty.experience_years = request.POST.get('experience_years')
        faculty.salary = request.POST.get('salary')
        faculty.joining_date = request.POST.get('joining_date')
        faculty.address = request.POST.get('address')

        faculty.user.save()
        faculty.save()

        return redirect('faculty_details_view', id=faculty.id)

    return render(request, 'edit_faculty.html', {
        'faculty': faculty,
        'roles': roles
    })

def delete_faculty_view(request, id):
    faculty = get_object_or_404(FacultyProfile, id=id)
    faculty.delete()
    return redirect('manage_faculties_view')