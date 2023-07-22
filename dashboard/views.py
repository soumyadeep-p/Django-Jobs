from django.shortcuts import render, redirect
from django.contrib import messages

def dashboard(request):
    if request.user.is_authenticated and request.user.is_verified:
        return render(request, 'dashboard/dashboard.html')
    else:
        messages.warning(request,'Please Log In to continue')
        return redirect(request, 'login')
# def proxy(request):
#     if request.user.is_applicant:
#         return redirect('applicant-dashboard')
#     elif request.user.is_recruiter:
#         return redirect('recruiter-dashboard')
#     else:
#         return redirect('login')
    
# def applicant_dashboard(request):
#     return render(request, 'dashboard/applicant_dashboard.html')

# def recruiter_dashboard(request):
#     return render(request, 'dashboard/recruiter_dashboard.html')
