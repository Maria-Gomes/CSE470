from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserRegisterForm, UserUpdateForm
from .models import Notification

# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)

        if user_form.is_valid():
            user_form.save()
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)

    context = {
        'user_form': user_form
    }

    return render(request, 'users/profile.html',context)

@login_required
def logout_view(request):
    Notification.objects.filter(to_user=request.user, notif_seen=True).delete()
    logout(request)

    return redirect('login')