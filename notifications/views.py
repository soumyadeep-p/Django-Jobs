from django.shortcuts import render, redirect
from .models import User, Notif
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def notifications (request):
    if request.user.is_authenticated:
        notifs = Notif.objects.filter(user=request.user).order_by('-timestamp') 
        context = {'notifs':notifs, 'user':request.user}
        return render(request, 'notifications/notifications.html', context)
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('dashboard')
    
