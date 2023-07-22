from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Company
from .form import UpdateCompanyForm
from users.models import User
from job.views import _delete_job
from job.models import Job

#function to create company
def update_company(request):
    if request.user.is_authenticated and request.user.is_recruiter and request.user.is_verified:
        company = Company.objects.get(user=request.user)
        if(request.method == 'POST'):
            form = UpdateCompanyForm(request.POST, instance=company)
            if form.is_valid():
                var = form.save(commit=False)
                user = User.objects.get(id=request.user.id)
                user.has_company = True
                var.save()
                user.save()
                messages.info(request, 'Your company info has been updated!')
                return redirect('dashboard')
            else :
                messages.warning(request, 'Something went wrong')
        else :
            form = UpdateCompanyForm(instance=company)
            context = {'form':form}
            return render(request, 'company/update_company.html', context)
    else: #check for applicant to not update/create company
        messages.warning(request,'Permission denied')
        return redirect('dashboard')

#view company details
def company_details(request,pk):
    company=Company.objects.get(pk=pk)
    context = {'company':company}
    return render(request , 'company/company_details.html', context)

def _delete_company(comp,user):
    jobs = Job.objects.filter(company = comp)
    for job in jobs:                                                                                            
        _delete_job(job)
    comp.delete()
    user.has_company = False
    Company.objects.create(user = user)
    user.save()
            
    

def delete_company(request):
    if request.user.is_authenticated and request.user.is_recruiter and request.user.is_verified and request.user.has_company:
        recruiter = User.objects.get(id=request.user.id)
        comp = Company.objects.get(user = recruiter)
        _delete_company(comp,recruiter)
        messages.warning(request, 'Your company has been deleted')
        return redirect('dashboard')
    else:
        messages.warning(request,'Permission denied')
        return redirect('dashboard')