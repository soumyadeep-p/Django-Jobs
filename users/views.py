from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from .form import RegisterUserForm
from resume.models import Resume
from company.models import Company
from company.views import _delete_company
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.conf import settings

def nice_hash(hash):
    new_hash = ""
    for x in hash:
        if x != '/':
            new_hash += str(x)
    return new_hash

def register_applicant(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            var = form.save(commit = False)
            var.is_applicant = True
            var.username = var.email
            var.is_verified = None
            var.email_hash = nice_hash(make_password(str(var.email) + str(var.id)))
            subject = 'Email-id verification'
            message = f'Please click on the following link to get your email-id {var.email} verified:\n http://localhost:8000/accounts/verify-user/{var.email_hash}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [var.email]
            try:
                send_mail (subject, message, from_email, recipient_list)
            except:
                messages.warning(request, f"Email-id does not exist")
                return redirect('register-applicant')
            else:
                var.save()
                Resume.objects.create(user=var)
                messages.info(request, 'Your account has been created! Please login')
                return redirect('login')
        else:
            print(form.errors)
            messages.warning(request, f"{form.errors}")
            return redirect('register-applicant')
    else:
        form = RegisterUserForm()
        context = {'form' : form}
        return render(request, 'users/register_applicant.html', context)
    
def register_recruiter(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            var = form.save(commit = False)
            var.is_recruiter = True
            var.username = var.email
            var.save()
            Company.objects.create(user = var)
            messages.info(request, 'Your account has been created! Please login')
            return redirect('login')
        else :
            messages.warning(request, f"{form.errors}")
            return redirect('register-recruiter')
    else:
        form = RegisterUserForm()
        context = {'form' : form}
        return render(request, 'users/register_recruiter.html', context)
    
def verify_user(request, pk):
    try:
        user = User.objects.get(email_hash = pk)
        user.is_verified = True
        user.save()
        return redirect('login')
    except:
        messages.warning(request, f"Verification unsuccessful")
        return redirect('home')

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username = email, password = password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong!')
            return redirect('login')
    else:
        return render(request, 'users/login.html')
    
def logout_user(request):
    logout(request)
    messages.info(request, 'Your session has ended')
    return redirect('login')

def delete_user(request):
    user = request.user
    logout(request)
    if user.is_recruiter and user.has_company:
        company = Company.objects.get(user = user)
        print(company.pk)
        _delete_company(company,user)
    user = User.objects.get(username = user)
    user.delete()
    messages.warning(request, 'Your account has been deleted')
    return redirect('login')
