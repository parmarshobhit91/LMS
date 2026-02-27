from django.shortcuts import render

# Create your views here.
def student_dashboard_view(request):
    return render(request, 'student-dashboard.html')