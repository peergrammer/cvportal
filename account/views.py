from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm

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
