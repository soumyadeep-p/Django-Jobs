from django.shortcuts import render, redirect
from .models import User, Notif
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect

def notifications (request):
    if request.user.is_authenticated and request.user.is_verified:
        notifs = Notif.objects.filter(user=request.user).order_by('-timestamp') 
        context = {'notifs':notifs, 'user':request.user}
        return render(request, 'notifications/notifications.html', context)
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('dashboard')
    
def delete_notification (request, pk):
    if request.user.is_authenticated and request.user.is_verified:
        notif = Notif.objects.get(user=request.user, pk = pk)
        notif.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('dashboard')