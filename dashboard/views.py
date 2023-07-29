from django.shortcuts import render, redirect
from django.contrib import messages

def dashboard(request):
    if request.user.is_authenticated and request.user.is_verified:
        return render(request, 'dashboard/dashboard.html')
    else:
        messages.warning(request,'Please Log In to continue')
        return redirect('login')