from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from .form import RegisterUserForm
from resume.models import Resume
from company.models import Company
from company.views import _delete_company
from resume.views import _delete_resume
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
    if request.user.is_authenticated and request.user.is_verified:
        messages.warning(request, 'You are already Logged In')
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            var = form.save(commit = False)
            user = User.objects.filter(email = var.email, is_verified = True)
            if user.exists():
                messages.warning(request, "Email-id already exists")
                return redirect('register-applicant')
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
            except Exception as e:
                messages.warning(request, f"Email-id does not exist")
                return redirect('register-applicant')
            else:
                var.save()
                messages.info(request, 'Please check your e-mail for user confirmation')
                return redirect('register-applicant')
        else:
            print(form.errors)
            messages.warning(request, f"{form.errors}")
            return redirect('register-applicant')
    else:
        form = RegisterUserForm()
        context = {'form' : form}
        return render(request, 'users/register_applicant.html', context)
    
def register_recruiter(request):
    if request.user.is_authenticated and request.user.is_verified:
        messages.warning(request, 'You are already Logged In')
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            var = form.save(commit = False)
            user = User.objects.filter(email = var.email, is_verified = True)
            if user.exists():
                messages.warning(request, "Email-id already exists")
                return redirect('register-applicant')
            var.is_recruiter = True
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
                return redirect('register-recruiter')
            else:
                var.save()
                messages.info(request, 'Please check your e-mail for user confirmation')
                return redirect('register-recruiter')
        else:
            print(form.errors)
            messages.warning(request, f"{form.errors}")
            return redirect('register-recruiter')
    else:
        form = RegisterUserForm()
        context = {'form' : form}
        return render(request, 'users/register_recruiter.html', context)
    
def verify_user(request, pk):
    if request.user.is_authenticated and request.user.is_verified:
        messages.warning(request, 'You are already Logged In')
        return redirect('dashboard')
    try:
        user = User.objects.get(email_hash = pk)
        user.is_verified = True
        user.save()
        if (user.is_applicant):
            Resume.objects.create(user = user)
        if (user.is_recruiter):
            Company.objects.create(user = user)
        duplicates = User.objects.filter(email = user.email, is_verified = None)
        for duplicate in duplicates:
            _delete_user(duplicate.id)
        login(request, user)
        return redirect('dashboard')
    except Exception as e:
        print(e)
        messages.warning(request, f"Verification unsuccessful")
        return redirect('home')

def login_user(request):
    if request.user.is_authenticated and request.user.is_verified:
        messages.warning(request, 'You are already Logged In')
        return redirect('dashboard')
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
    if request.user.is_authenticated and request.user.is_verified:
        logout(request)
        messages.info(request, 'Your session has ended')
        return redirect('login')
    else:
        messages.warning(request, 'Please Log In to continue')
        return redirect('login')

def _delete_user(pk):
    user = User.objects.get(id = pk)
    if user.is_recruiter and user.has_company:
        company = Company.objects.filter(user = user)
        if company.exists():
            _delete_company(company[0],user)
    if user.is_applicant:
        resume = Resume.objects.filter(user=user)
        if resume.exists():
            _delete_resume(resume[0], user)
    user.delete()

def delete_user(request):
    if request.user.is_authenticated and request.user.is_verified:
        user = request.user
        logout(request)
        _delete_user(user.id)
        messages.warning(request, 'Your account has been deleted')
        return redirect('login')
    else:
        messages.info(request, 'Please Log In to continue')
        return redirect('login')