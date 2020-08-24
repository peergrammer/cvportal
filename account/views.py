from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(request, 
                            username=cleaned_data['username'],
                            password=cleaned_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponse('Successfully logged')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    
    return render(request, 'account/login.html', {'form': form})

@login_required
def panel(request):
    return render(request, 'account/panel.html', {'section': 'panel'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False) #dont commit yet
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})