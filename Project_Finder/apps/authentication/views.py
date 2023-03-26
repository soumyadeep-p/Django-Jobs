from django.shortcuts import render
from django.http import HttpResponse
from .forms import ProfileForm

# Create your views here.
def home(request):
	return HttpResponse('hello world')

def signup(request):
	if request.method == "POST":
		form = ProfileForm(request.POST or None)
		if form.is_valid():
			form.save()
		print("*****SAVED*****")
	return render(request, 'signup.html')

def signin(request):
	return render(request, 'signin.html')
	