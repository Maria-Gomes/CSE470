from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm

# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
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